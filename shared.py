import random
from itertools import islice
from heapq import nlargest


def flatten(transcript):
    """flatten the transcript into a list"""
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


def word_count(flat_transcript):
    """count number of words in flat transcript"""
    cnt = 0
    word_indx = [] # initialise list of all the word indices
    for i in range(len(flat_transcript)):        
        if type(flat_transcript[i]) is dict:
            if flat_transcript[i]['type'] == 'word':
                cnt +=1    
                word_indx.append(i) # add word indices here and you won't need to go through the transcript once again to collect them
    return cnt, word_indx


def random_words_list(flat_transcript, rate): 
    """create a list of random words from transcript for deletion/substitution/insertion"""
    total_words, indx = word_count(flat_transcript)
    words = int(total_words * rate)
    indx = random.sample(population=indx, k=words) # select random indices for deletion from the list of all word indices
    words_list = []
    for i in indx:
        words_list.append(flat_transcript[i]['value'])
    return words_list


def create_one_gram_list():
    """create a list of unigrams"""
    one_gram=[]
    with open('../lm_unpruned', 'r') as f:
        for line in islice(f, 8, 42159, 1): #read in words only from 1-gram list
            if line.split(' ')[1] not in ('<unk>', '</s>'):
                one_gram.append([float(line.split(' ')[0]), line.split(' ')[1].replace("\n", '')])   
    return one_gram

one_gram_list = create_one_gram_list()
reduced_one_gram = nlargest(2000, one_gram_list) 