import nltk
from itertools import islice

#read in 1-gram words from the dictionary
def read_one_gram():
    one_gram=[]
    one_gram_list =[]
    with open('C:/temp/lm_unpruned', 'r') as f:
        for line in islice(f, 6, 42159, 1):
            one_gram.append(line)
    for i in range(len(one_gram)):
                one_gram_list.append(one_gram[i].split(' '))
    return one_gram_list
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
                final_sound = ""
                final_sound_switch = 0
                for j in syllables:
                    if "1" in j:
                        final_sound_switch = 1
                        final_sound += j
                    elif final_sound_switch == 1:
                        final_sound += j
            cmu_final_sound_dict[word.lower()] = final_sound
    return cmu_final_sound_dict

phonemic_model = create_cmu_sound_dict()

#DRAFT - iterate through the 1-gram list to calculate Levenshtein distance against word 'dragon'. Does not work at the moment
for sublist in one_gram_list:  
    if sublist[1] not in ['<s>', '</s>\n', 'year', 'florals', 'flax\n', 'f._i._v.', 'f._i._m._a.', 'f._f._a.', "f._b._i.'s", 'f._a._s._d.', 'f._a._f._b.', 'espressos', 'emulates'] :
        test = nltk.edit_distance(phonemic_model["dragon"], phonemic_model[sublist[1]], transpositions = False)
print(test) 
