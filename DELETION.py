import pandas as pd
import json
import random

#read in csv file, delete 20% of words from json manual transcript, output csv with altered manual transcript as new column
df = pd.read_csv('C:/temp/ASRforAD.csv')
#df['json_with_deletion'], df['json_deleted_words'] = df.apply(lambda df : pd.Series(test_fn(df['json_utterances_man'])), axis =1)
df['json_man_with_deletion'] = df.apply(lambda df : del_fn(df['json_utterances_man']), axis =1)
df.to_csv('C:/temp/DELETION_ASRforAD.csv')

print(df.head())
print(len(df.iloc[2,5]))
print(df.iloc[2,5])


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
        for i in sublist['tokens']:
            flat_list.append(i)            
    return flat_list

# function to count number of words in transcript
def word_count(transcript):
    cnt = 0
    for i in range(len(transcript)):
        if transcript[i]['type'] == 'word':
            cnt +=1    
    return cnt

#delete random words from the transcript, return new transcript
def del_words(transcript, del_rate): 
    total_words = word_count(transcript)
    del_words = int(total_words * del_rate)
    del_indx=[]
    del_w = []
    while len(del_indx) < del_words:
        r=random.randint(0,total_words)
        if r not in del_indx:                
            if transcript[r]['type'] == 'word':
                del_indx.append(r)
                del_w.append([transcript[r]])
    del_indx.sort()
    new_tr = []    
    for i in range (len(transcript)):
        if i not in del_indx:          
            new_tr.append(transcript[i])
    return new_tr
