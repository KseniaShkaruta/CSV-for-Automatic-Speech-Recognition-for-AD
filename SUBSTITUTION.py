import pandas as pd
import json 
import random
import nltk
from itertools import islice
from heapq import nsmallest

#read in csv file, delete 20% of words from json manual transcript, output csv with altered manual transcript as new column
df = pd.read_csv('../../ASRforAD.csv')

df = df.merge(df.json_utterances_man.apply(lambda s: pd.Series(subst_fn(s))), left_index=True, right_index=True)
df.rename(columns = {0:'json_utterances_man_with_SUBSTITUTED_WORDS', 1:'SUBSTITUTED_WORDS'}, inplace =True )

df.to_csv('C:/temp/DELETION_ASRforAD.csv')

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
def words_to_subst(flat_transcript, subst_rate): 
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

#create a list of the words to use for substitution, return both lists: words_to_substitute, substitute_with
def subst_with(transcript):
    one_gram_list = reduced_one_gram_list() 
    phonemic_model = create_cmu_sound_dict()
    words_to_substitute = words_to_subst(flatten(transcript), 0.2)
    substitute_with = []
    for j in range(len(words_to_substitute)):
        if words_to_substitute[j] not in phonemic_model:
            r=random.randint(0,len(one_gram_list)-1)
            substitute_with.append(one_gram_list[r])
        else:
            dist_list = []
            wd_list = []    
            for i in range(len(one_gram_list)):
                if one_gram_list[i] != words_to_substitute[j]:
                    if one_gram_list[i] in phonemic_model:                
                        dist_list.append(nltk.edit_distance(phonemic_model[words_to_substitute[j]], phonemic_model[one_gram_list[i]], transpositions = False))#calculate Levenstein distance
                        wd_list.append(one_gram_list[i])                   
                    else:
                        dist_list.append(99)
                        wd_list.append('NOT_IN_DICTNRY') 
                else:
                    dist_list.append(100)
                    wd_list.append('SAME_WORD')
            substitute_with.append(wd_list[dist_list.index(min(dist_list))])#pick with word that had the smallest Levenstein distance
    return words_to_substitute, substitute_with

#substitute words in the transcript, return the new transcript and list of substituted words
def subst_words(transcript):
    to_substitute, substitute_with = subst_with(transcript)
    substituted_words =[]
    i = 0 
    try:
        while i != (len(to_substitute)):
            for sublist in transcript: 
                i = 0
                for element in sublist['tokens']:
                    if element['type'] == 'word':   
                        if element['value'] == to_substitute[i]:  #find word that needs to be substituted in transcript                        
                            substituted_words.append(element['value'])
                            element['value'] = substitute_with[i]
                            to_substitute.remove(to_substitute[i])
                            substitute_with.remove(substitute_with[i])                            
    except:
        pass
    return transcript, substituted_words
 

    
