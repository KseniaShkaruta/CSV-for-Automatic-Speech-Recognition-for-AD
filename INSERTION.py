from itertools import islice
from heapq import nlargest

#store bi-gram as a list of lists of three elements: word, following word and probability of occurance of the following word
bi_gram=[]
with open('../lm_unpruned', 'r') as f:
    for line in islice(f, 57292, 1380576, 1): #read in words only from 1-gram list
        bi_gram.append([float(line.split(' ')[0]), line.split(' ')[1], line.split(' ')[2].replace("\n", '')])
        
"""Quick stats
2,000 - 100% unique, 1,598 after cleaning
3,000 - 99.8% unique, 3 repeating word, 2,190 after cleaning
4,000 - 99.5% unique, 10 repeating word, 2,914 after cleaning
5,000 - 99.12% unique, 22 repeating word, 3,363 after cleaning
6,000 - 99.3% unique, 22 repeating word, 3,363 after cleaning
7,000 - 99.4% unique, 22 repeating word, 4,113 after cleaning
8,000 - 99.4% unique, 22 repeating word, 4,987 after cleaning


#For 2,000 - 100% unique, 1,598 after cleaning
words = nlargest(2000, bi_gram)
unique = []
repeat = []
for i in range(len(words)):
    if words[i][1] not in unique:
        unique.append(words[i][1])
    else:
        print(words[i])

#code to clean the bi-gram list 
reduced = []
for i in range(len(words)):
    if "_" not in words[i][1]:
        if words[i][2] != '<unk>':
            if words[i][2] != '</s>':
                reduced.append(words[i])
print(len(unique))
print(repeat)
print(len(reduced))


#For 3,000 - 2,994 unique, 3 - repeating
words = nlargest(3000, bi_gram)
unique = []
repeat = []
for i in range(len(words)):
    if words[i][1] not in unique:
        unique.append(words[i][1])
    else:
        print(words[i])
        
#code to clean the bi-gram list 
reduced = []
for i in range(len(words)):
    if "_" not in words[i][1]:
        if words[i][2] != '<unk>':
            if words[i][2] != '</s>':
                reduced.append(words[i])
print(len(unique))
print(repeat)
print(len(reduced))

#For 8,000 - 7,948 unique, 26 - repeating
words = nlargest(8000, bi_gram)
unique = []
repeat = 0
for i in range(len(words)):
    if words[i][1] not in unique:
        unique.append(words[i][1])
    else:
        print(words[i])
        repeat +=1
        
#code to clean the bi-gram list 
reduced = []
for i in range(len(words)):
    if "_" not in words[i][1]:
        if words[i][2] != '<unk>':
            if words[i][2] != '</s>':
                reduced.append(words[i])
                
print(len(unique))
print(repeat)
print(len(reduced))

for i in range(len(reduced)):
    print(reduced[i])
