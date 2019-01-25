import pandas as pd
import json
import random

#read in csv file, delete 20% of words from json manual transcript, output csv with altered manual transcript as new column
df = pd.read_csv('C:/temp/ASRforAD.csv')
df = df.merge(df.json_utterances_man.apply(lambda s: pd.Series(del_fn(s))), left_index=True, right_index=True)
df.to_csv('C:/temp/DELETION_ASRforAD.csv')

print(df.head())

# main fn 
def del_fn(df):
    return del_words(flatten(store_tr(df)), 0.2)

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
def word_count(transcript):
    cnt = 0
    for i in range(len(transcript)):        
        if type(transcript[i]) is dict:
            if transcript[i]['type'] == 'word':
                cnt +=1    
    return cnt

#delete random words from the transcript, return new transcript and the list of deleted words
def del_words(transcript, del_rate): 
    total_words = word_count(transcript)
    del_words = int(total_words * del_rate)
    del_indx=[]
    del_w = []
    while len(del_indx) < del_words:
        r=random.randint(0,total_words)
        if r not in del_indx:
            if type(transcript[r]) is dict:
                if transcript[r]['type'] == 'word':
                    del_indx.append(r)
                    del_w.append([transcript[r]])
        del_indx.sort()
    new_tr = []    
    for i in range (len(transcript)):
        if i not in del_indx:          
            new_tr.append(transcript[i])
    return del_w, new_tr
