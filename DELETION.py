import pandas as pd
import json
import random


#read in csv file and store manual transcript in temp value
df = pd.read_csv('C:/Users/toshiba/Documents/test.csv')
print(df.head(3))
tr = json.loads(df.iloc[0,2])

#function to flatten the transcript list
def flatten(transcript):    
    flat_list = []
    for sublist in transcript: 
        for i in sublist['tokens']:
            flat_list.append(i)
    return flat_list

flat_tr = flatten(tr)
print(len(flat_tr))

# function to count number of words in transcript
def word_count(transcript):
    cnt = 0
    for i in range(len(transcript)):
        if transcript[i]['type'] == 'word':
            cnt +=1    
    return cnt

num_words = word_count(flat_tr)
print(num_words)

#create two lists: 1.deleted words, 2. indeces of deleted words
del_rate = 0.2
del_words = int(num_words * del_rate)
ind_list=[]
del_w = []

while len(ind_list) < del_words:
    r=random.randint(0,num_words)
    if r not in list:                
        if flat_tr[r]['type'] == 'word':
            ind_list.append(r)
            del_w.append([flat_tr[r]])
    
print(len(ind_list))
print(len(del_w))
print(del_w)
print(ind_list)

#create new transcript without the deleted words
def new_tr(transcript, del_indx):    
    del_indx.sort()
    new_tr = []
    m = 0
    i = 0
    for i in range (len(transcript)):
        if i not in del_indx:          
            new_tr.append(transcript[i])
    return new_tr
