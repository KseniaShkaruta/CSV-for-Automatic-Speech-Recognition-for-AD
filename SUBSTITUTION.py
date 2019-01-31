import nltk
from itertools import islice

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
 
