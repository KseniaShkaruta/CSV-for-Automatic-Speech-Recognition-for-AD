# CSV for Automatic Speech Recognition for People with Alzheimer's Disease
Manipulation of csv and json files to delete/insert/substitute words from/into manual speech transcripts. Altered transcripts will be used to improve the performance of the automatic speech recognition (ASR).


## Getting Started
Code was written in Python in Jupyter Labs. 
You can install from here (conda is recommended): https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html

### Prerequisites
You will need the following Python libraries:
- pandas
- json
- random
- nltk
- itertools
- heapq

You will need the following files:
- Uni-gram and bi-gram words to substitute with the most similar word(uni-gram) and insert the word that is most likely to follow (bi-gram)
- [c-06d](http://www.greenteapress.com/thinkpython/code/c06d?fbclid=IwAR3kK8u0l48ksaGi8v60FZLDsSjpdjhw3dCCeZdRDS0VkBhgeR5YyzSUTuI) to create a dictionary of phonemic models


## Code
Code is broken down into the following files:

### 1.	Shared.py
- Manual transcripts were in json format – use `json.loads` in `store_tr(df)` to store them
- Function `flatten(tr)` flattens the stored transcript to do the `word_count(fl_tr)` to determine how many words need to be altered at a certain rate (0.2, 0.4, 0.6) and create a list of these words at random by `random_words_list(fl_tr, rate)`
- `create_one_gram_list()` creates a list of uni-grams with the associated probability of this word to appear in text/speech. A reduced list of 2,000 most used words created for the transcript unigram dictionary in substitution file

### 2.	Deletion.ipynb
- Delete words from manual transcript that match those on the `random_words_list(fl_tr, rate)`

### 3.	Substitution.ipynb
- `create_cmu_sound_dict()` creates a dictionary of phonemic model of words. This will be used to calculate the Levenstein distance between the words to pick the most phonemically similar word for substitution
- Ideally, the substitution function would calculate a Levenstein distance for a word to substitute from `random_words_list(fl_tr, rate)` and each word from the `one_gram_list` that was created by `create_one_gram_list()` and pick the word with the shortest distance for substitution. However, the processing time of this function was too long (~80 seconds to process 1,000 words on a standard CPU computer). Therefore, a design decision was made to create a dictionary for all unique words from all manual speech transcripts with the words as keys and word with shortest Levenstein distance along with the distance itself as list of values - `create_tr_unigram_dict()`.
- Note, that transcript had several cases of Unicodes within the word values, a decision not to clean those was made based on the assumption that a transcript should be going through cleansing and this code should not do this. Since these cases would not match any word in `one_gram_list` a random value is returned for substitution
- Note, to reduce processing time a `reduced_one_gram` list is used that contains 2,000 most used words

### 4.	Insertion.ipynb
- `create_bi_gram_dict(bi_gram_list)` that stores words as keys and corresponding words with the probability of this word to follow as a list of values. 
- Use words from `random_words_list(fl_tr, rate)` as a reference for insertion a new word i.e. insert after that word. To determine which words to insert use `bi_gram_dict` – insert most likely word to follow (i.e. highest probability) if it does not match the following word in transcript, else insert the next most probable word. If word is not found in bi-gram insert a random word from uni-gram

