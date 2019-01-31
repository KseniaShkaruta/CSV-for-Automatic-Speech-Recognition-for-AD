import pandas as pd
import json
import random

#read in csv file, delete 20% of words from json manual transcript, output csv with altered manual transcript and list of deleted words as new columns
df = pd.read_csv('C:/temp/ASRforAD.csv')
df = df.merge(df.json_utterances_man.apply(lambda s: pd.Series(del_fn(s))), left_index=True, right_index=True)
df.rename(columns = {0:'json_utterances_man_wt_DELETED_WORDS', 1:'DELETED_WORDS'}, inplace =True )
df.to_csv('C:/temp/DELETION_ASRforAD.csv')

print(df.head())

# main fn 
def del_fn(df):
    return del_words(store_tr(df))

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
    word_indx = [] # initialise list of all the word indices
    for i in range(len(flat_transcript)):        
        if type(flat_transcript[i]) is dict:
            if flat_transcript[i]['type'] == 'word':
                cnt +=1    
                word_indx.append(i) # add word indices here and you won't need to go through the transcript once again to collect them
    return cnt, word_indx

#create a list of words to delete from transcript using random seed
def list_del_words(flat_transcript, del_rate): 
    total_words, word_indx = word_count(flat_transcript)
    del_words = int(total_words * del_rate)
    del_indx = random.sample(population=word_indx, k=del_words) # select random indices for deletion from the list of all word indices
    del_w = []
    for i in del_indx:
        del_w.append(flat_transcript[i])
    return del_w

#delete words from the transcript, return the new transcript and list of deleted words
def del_words(transcript):
    to_delete = list_del_words(flatten(transcript), 0.2)
    deleted_words = []        
    i = 0
    try:
        while i != (len(to_delete)):
            for sublist in transcript: 
                for element in sublist['tokens']:
                    if to_delete[i] == element:                  
                        deleted_words.append(element)
                        to_delete.remove(to_delete[i])
                        sublist['tokens'].remove(element)                       
            i =0
    except:
        pass
    return transcript, deleted_words
