import pandas as pd
import json 
import random
from itertools import islice
from heapq import nlargest


#read in csv file, words from bigram/unigram into json manual transcript, output csv with altered manual transcript and inserted words as new columns 
df = pd.read_csv('../ASRforAD.csv')

df = df.merge(df.json_utterances_man.apply(lambda s: pd.Series(insrt_fn(s, 0.2))), left_index=True, right_index=True)
df.rename(columns = {0:'json_utterances_man_with_INSERTED_WORDS', 1:'INSERTED_WORDS'}, inplace =True )
df.to_csv('../INSERTION_ASRforAD.csv')

print(df.head())


# main fn
def insrt_fn(df, rate):
    return insert_words(store_tr(df), rate)

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

#create a list of random words from transcript for deletion/substitution/insertion
def random_words_list(flat_transcript, rate): 
    total_words, indx = word_count(flat_transcript)
    words = int(total_words * rate)
    indx = random.sample(population=indx, k=words) # select random indices for deletion from the list of all word indices
    words_list = []
    for i in indx:
        words_list.append(flat_transcript[i]['value'])
    return words_list


#store bi-gram as a list of lists of three elements: word, following word and probability of occurance of the following word
def read_bi_gram():
    bi_gram=[]
    
    with open('../lm_unpruned', 'r') as f:
        for line in islice(f, 57292, 1380576, 1): #read in words only from 1-gram list
            if line.split(' ')[1] not in ('<unk>', '</s>') and '_' not in line.split(' ')[1] and line.split(' ')[2].replace("\n", '') not in ('<unk>', '</s>') and '_' not in line.split(' ')[2].replace("\n", ''):
                bi_gram.append([float(line.split(' ')[0]), line.split(' ')[1], line.split(' ')[2].replace("\n", '')])    
    return bi_gram

bi_gram_list = read_bi_gram()


#create bi-gram dictionary based on the list of bi-grams
def create_bi_gram_dict(bi_gram_list):
    bi_gram_dict = {}

    for i in range(len(bi_gram_list)): 
        if bi_gram_list[i][1] in bi_gram_dict.keys():  
            bi_gram_dict[bi_gram_list[i][1]].append([bi_gram_list[i][0], bi_gram_list[i][2]])  
        else:  
            bi_gram_dict[bi_gram_list[i][1]] = [[bi_gram_list[i][0], bi_gram_list[i][2]]]    
    return bi_gram_dict  

bi_gram_dict = create_bi_gram_dict(bi_gram_list)


#create a 1-gram words list
def create_one_gram_list():
    one_gram=[]
    with open('../lm_unpruned', 'r') as f:
        for line in islice(f, 8, 42159, 1): #read in words only from 1-gram list
            if line.split(' ')[1] not in ('<unk>', '</s>'):
                one_gram.append([float(line.split(' ')[0]), line.split(' ')[1].replace("\n", '')])   
    return one_gram

one_gram_list = create_one_gram_list()


#insert words into the transcript from bi-gram/uni-gram dictionaries, return the new transcript and list of inserted words
def insert_words(transcript, rate):
    to_insert = rand_words_list(flatten(transcript), rate)
    inserted_words = []        
    try:
        while 0 != (len(to_insert)):            
            for sublist in transcript: 
                for element in sublist['tokens']:                
                    if element['type'] not in('REF', 'INS', 'INS_SEC', 'RND'):      #avoid manipulating words that were already altered i.e. inserted or inserted after                     
                        if to_insert[0] == element['value']:                             
                            to_insert.remove(to_insert[0])                  #remove word from the list, the next element becomes index 0 and will be looked at once this loop is complete              
                            if element['value'].lower() in bi_gram_dict:
                                if len(bi_gram_dict[element['value'].lower()]) > 1:         #check that bi-gram key has more than one value    
                                    first_max, second_max = nlargest(2, bi_gram_dict[element['value'].lower()])                #store two words fist_max/second_max that are more likely to occure according to bi-gram dictionary
                                    if sublist['tokens'].index(element) == len(sublist['tokens'])-1:            #if the word after wich we need to insert is the last in the token, insert first_max                                                                            
                                        sublist['tokens'].insert(sublist['tokens'].index(element)+1, {'type': 'INS', 'value': first_max[1]})                  #change 'type' to INS so the word is not used as a reference for insertion in future loops
                                        element['type'] = 'REF'             #change 'type' of the word that was used as a reference for insertion so not to use it for other insertions
                                        inserted_words.append({'type': 'word', 'value': first_max[1]})                                           
                                    else:
                                        if first_max[1] != sublist['tokens'][sublist['tokens'].index(element)+1]['value'].lower():      #check if the first_max from bi-gram is the same as the word following the word that we use as a reference for insertion                                          
                                            sublist['tokens'].insert(sublist['tokens'].index(element)+1, {'type': 'INS', 'value': first_max[1]})
                                            element['type'] = 'REF'   
                                            inserted_words.append({'type': 'word', 'value': first_max[1]})  
                                            
                                        else:                                                                  #insert second_max, second most probable word from bi-gram dict                                                                                  
                                            sublist['tokens'].insert(sublist['tokens'].index(element)+1, {'type': 'INS_SEC', 'value': second_max[1]})
                                            element['type'] = 'REF'
                                            inserted_words.append({'type': 'word', 'value': second_max[1]})                                          
                                else:                                                                    
                                    sublist['tokens'].insert(sublist['tokens'].index(element)+1, {'type': 'INS', 'value': max(bi_gram_dict[element['value'].lower()])[1]})
                                    element['type'] = 'REF'    
                                    inserted_words.append({'type': 'word', 'value': max(bi_gram_dict[element['value'].lower()])[1]})                                  
                            else:                             
                                subst_w = random.choice(one_gram_list)[1]                             #if the word not in bi-gram use insert a random word from uni-gram
                                sublist['tokens'].insert(sublist['tokens'].index(element)+1, {'type': 'RND', 'value': subst_w})
                                element['type'] = 'REF'
                                inserted_words.append({'type': 'word', 'value': subst_w})                              
    except:
        pass

    for sublist in transcript: 
        for element in sublist['tokens']:
            if element['type'] in('REF', 'INS', 'INS_SEC', 'RND'):
                element['type'] = 'word'
    return json.dumps(transcript), inserted_words
