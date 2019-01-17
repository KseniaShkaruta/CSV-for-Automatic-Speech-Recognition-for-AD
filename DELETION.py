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
        for i in range(len(sublist['tokens'])):
            flat_list.append(sublist['tokens'][i])
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

#generate list with random numbers
def del_list(num_words, del_rate):    
    del_words = int(num_words * del_rate)
    list=[]
    while len(list) < del_words:
        r=random.randint(0,num_words)
        if r not in list: 
            list.append(r)
    list.sort()
    return list

del_indx = del_list(num_words, 0.2)
print(del_indx)
    
m = 0
i = 0
temp = []
if len(temp) < (len(del_indx)):
    if flat_tr[del_indx[i]]['type'] == 'word':
        temp.append([flat_tr[del_indx[i]]])
        i +=1
       
print(len(temp))
print(temp)
