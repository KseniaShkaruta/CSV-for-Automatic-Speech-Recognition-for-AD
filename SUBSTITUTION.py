import nltk
from itertools import islice
import pandas as pd
import json 
import random

#read in csv file, delete 20% of words from json manual transcript, output csv with altered manual transcript as new column
df = pd.read_csv('C:/temp/ASRforAD.csv')

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

#count number of words in transcript
def word_count(flat_transcript):
    cnt = 0
    for i in range(len(flat_transcript)):        
        if type(flat_transcript[i]) is dict:
            if flat_transcript[i]['type'] == 'word':
                cnt +=1    
    return cnt

#create a list of random words to substitute in transcript 
def subst_words_list(flat_transcript, subst_rate): 
    total_words = word_count(flat_transcript)
    subst_words = int(total_words * subst_rate)
    subst_indx=[]
    subst_w = []
    while len(subst_indx) < subst_words:
        r=random.randint(0,total_words)
        if r not in subst_indx:
            if type(flat_transcript[r]) is dict:
                if flat_transcript[r]['type'] == 'word':
                    subst_indx.append(r)
                    subst_w.append(flat_transcript[r]['value'])    
    return subst_w

subst_list = subst_words_list(flatten(store_tr(df.iloc[0,2])), 0.2)

#read in 1-gram words from the dictionary
def read_one_gram():
    one_gram=[]
    one_gram_list =[]
    with open('C:/temp/lm_unpruned', 'r') as f:
        for line in islice(f, 8, 42159, 1):
            one_gram.append(str(line.splitlines()).split(' ')[1].replace(']',''))    
    return one_gram
one_gram_list = read_one_gram()
print(one_gram_list)

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

phonemic_model = create_cmu_sound_dict()

#return the substitution list 
def subst_list(words_to_substitute):
    final_list = []
    for j in range(len(words_to_substitute)):
        if subst_list[j] not in phonemic_model:
            r=random.randint(0,len(one_gram_list)-1)
            final_list.append(one_gram_list[r])
        else:
            dist_list = []
            wd_list = []    
            for i in range(len(one_gram_list)):
                if one_gram_list[i] != subst_list[j]:
                    if one_gram_list[i] in phonemic_model:                
                        dist_list.append(nltk.edit_distance(phonemic_model[subst_list[j]], phonemic_model[one_gram_list[i]], transpositions = False))
                        wd_list.append(one_gram_list[i])                   
                    else:
                        dist_list.append(99)
                        wd_list.append('NOT_IN_DICTNRY') 
                else:
                    dist_list.append(100)
                    wd_list.append('SAME_WORD')
            final_list.append(wd_list[dist_list.index(min(dist_list))])
    return final_list
