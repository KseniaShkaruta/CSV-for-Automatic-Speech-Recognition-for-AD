from itertools import islice
from heapq import nlargest

#main function
temp = create_bi_gram_dict(bi_gram_list)
print(len(temp))

#store bi-gram as a list of lists of three elements: word, following word and probability of occurance of the following word
def read_bi_gram():
    bi_gram=[]
    
    with open('../lm_unpruned', 'r') as f:
        for line in islice(f, 57292, 1380576, 1): #read in words only from 1-gram list
            if line.split(' ')[1] not in ('<unk>', '</s>') and '_' not in line.split(' ')[1] and line.split(' ')[2].replace("\n", '') not in ('<unk>', '</s>') and '_' not in line.split(' ')[2].replace("\n", ''):
                bi_gram.append([float(line.split(' ')[0]), line.split(' ')[1], line.split(' ')[2].replace("\n", '')])
    
    return bi_gram

bi_gram_list = read_bi_gram()
print(len(bi_gram))


#create bi-gram dictionary based on the list of bi-grams
def create_bi_gram_dict(bi_gram_list):
    bi_gram_dict = {}

    for i in range(len(bi_gram)): 
        if bi_gram[i][1] in bi_gram_dict.keys():  
            bi_gram_dict[bi_gram[i][1]].append([bi_gram[i][0], bi_gram[i][2]])  
        else:  
            bi_gram_dict[bi_gram[i][1]] = [[bi_gram[i][0], bi_gram[i][2]]]
    
    return bi_gram_dict 
