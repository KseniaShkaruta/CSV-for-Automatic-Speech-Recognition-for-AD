import pandas as pd
import json 
import random
import nltk
from itertools import islice
from heapq import nsmallest

#read in csv file, delete 20% of words from json manual transcript, output csv with altered manual transcript as new column
df = pd.read_csv('../ASRforAD.csv')

df = df.merge(df.json_utterances_man.apply(lambda s: pd.Series(subst_fn(s))), left_index=True, right_index=True)
df.rename(columns = {0:'json_utterances_man_with_SUBSTITUTED_WORDS', 1:'SUBSTITUTED_WORDS'}, inplace =True )

df.to_csv('../SUBSTITUTION_ASRforAD.csv')

print(df.head())

# main fn
def subst_fn(df):    
    return subst_words(store_tr(df))

#store json transcript
def store_tr(df_row):       
    tr = json.loads(df_row)
    return tr

#flatten the transcript list
def flatten(transcript):
    flat_list = []
    for sublist in transcript:
        for item in sublist:
            if item == 'tokens':
                flat_list.append(item)
                for item in sublist['tokens']:
                    flat_list.append(item)   
            else:
                flat_list.append(item)
                flat_list.append(str(sublist['start_time']))
    return flat_list

#count number of words in transcript, return the count and the list of the words' indecies
def word_count(flat_transcript):
    cnt = 0
    word_indx = [] # initialise list of all the word indices
    for i in range(len(flat_transcript)):        
        if type(flat_transcript[i]) is dict:
            if flat_transcript[i]['type'] == 'word':
                cnt +=1    
                word_indx.append(i) # add word indices here and you won't need to go through the transcript once again to collect them
    return cnt, word_indx

#create a list of random words to substitute in transcript 
def words_to_subst_fn(flat_transcript, subst_rate): 
    total_words, word_indx = word_count(flat_transcript)
    subst_words = int(total_words * subst_rate) #how many words need to be substituted
    subst_indx=random.sample(population=word_indx, k=subst_words) # select random indices for deletion from the list of all word indices
    subst_w = []
    for i in subst_indx:        
        subst_w.append(flat_transcript[i]['value'])   
    return subst_w


#read in 1-gram words from the dictionary, return 2,000 most common words
def reduced_one_gram_list():
    one_gram=[]
    one_gram_list =[]
    with open('C:/temp/lm_unpruned', 'r') as f:
        for line in islice(f, 8, 42159, 1): #read in words only from 1-gram list
            one_gram.append([int(''.join(e for e in (str(line.splitlines()).split(' ')[0]) if e.isalnum())), str(line.splitlines()).split(' ')[1].replace(']','').replace('[','')])
    one_gram.remove([159267, '<unk>']) #remove uknown value from the list
    temp = nsmallest(2000, one_gram) #pick top 2,000 most frequent words in order to reduce the size of the 1-gram dict
    for i in temp:
        one_gram_list.append(i[1]) #store only words
    return one_gram_list

#create phonetic dictionary
def create_cmu_sound_dict():
    cmu_final_sound_dict = {}
    with open('C:/temp/c06d') as cmu_dict:
        cmu_dict = cmu_dict.read().split("\n")
        for i in cmu_dict:
            i_s = i.split()
            if len(i_s) > 1:
                word = i_s[0]
                syllables = i_s[1:]
            cmu_final_sound_dict[word.lower()] = " ".join(syllables)
    return cmu_final_sound_dict

#read in unigrams from all the transcripts into a unique list
def create_tr_unigrm():
    tr_unigrm_unique = []
    with open('../tr_unigrams.txt', 'r') as tr_unigrm:
        tr_unigrm = tr_unigrm.read().replace('"','').replace("\\\\u2019", "'").replace('\\\\n', '').replace("\\\\t", "").replace("\\\\u00e9", "é").replace("\\\\u00e1", "á").replace("\\\\u00ef", "ï").replace("\\\\u02dc", "~").replace("\\\\u2018", "'").replace("\\\\u2026", "...").replace("\\\\","")
        tr_unigrm = tr_unigrm.split(", ")
        for i in range(len(tr_unigrm)):
            if tr_unigrm[i] not in tr_unigrm_unique:
                tr_unigrm_unique.append(tr_unigrm[i])
    return tr_unigrm_unique

#create a dictionary for all the unique unigrams from all the transcripts unigram dictionary. Dictionary will contain corresponding word with a minimum Levenstein distance as well as the distance itself
def create_tr_unigram_dict():
    tr_unigrm = create_tr_unigrm()    
    one_gram_list = create_one_gram_list()
    phonemic_model = create_cmu_sound_dict()
    tr_unigrm_dict = {}
    for j in range(len(tr_unigrm)):
        if tr_unigrm[j] not in phonemic_model:
            r=random.randint(0,len(one_gram_list)-1)    #if  unigram from transcript dictionary not in phonemic model return a random value from the unigram list
            tr_unigrm_dict[tr_unigrm[j]] = [one_gram_list[r], -1]   #set distance to -1      
        else:                
            temp_sub = []
            temp_dist = []
            for i in range(len(one_gram_list)):
                if tr_unigrm[j] != one_gram_list[i]:
                    if one_gram_list[i] in phonemic_model: 
                        temp_dist.append(nltk.edit_distance(phonemic_model[tr_unigrm[j]], phonemic_model[one_gram_list[i]], transpositions = False))
                        temp_sub.append(one_gram_list[i])
                    else:
                        temp_dist.append(99)
                        temp_sub.append('NOT_IN_DICTNRY') 
                else:
                    temp_dist.append(100)
                    temp_sub.append('SAME_WORD')
            tr_unigrm_dict[tr_unigrm[j]] = [temp_sub[temp_dist.index(min(temp_dist))], min(temp_dist)]
    return tr_unigrm_dict

#function to substitute the words in transcript. Substitute words that are in the random substitution list with the values from the tr_unigram_dictionary 
def subst_words(transcript):
    tr_unigrm_dict = create_tr_unigram_dict()
    words_to_sub = words_to_subst_fn(flatten(transcript), 0.2)
    substituted_words =[]
    i = 0
    try:
        while i != (len(words_to_sub)):
            for sublist in transcript:                 
                for element in sublist['tokens']:
                    if element['type'] == 'word':                 
                        if element['value'] == words_to_sub[i]:
                            substituted_words.append(element['value']) 
                            element['value'] = final_dict[words_to_sub[i]][0]
                            words_to_sub.remove(words_to_sub[i])                            
            i = 0   

    except:
        pass
    return transcript, substituted_words
