# Automatic-Speech-Recognition-for-AD
Manipulation of csv and json files to delete/insert/substitute words from/into manual speech transcripts. Altered transcripts will be used to improve the performance of the ASR (automatic speech recognition).


## Getting Started
Code was written in Python in Jupyter Labs. 
You can install from here (conda is recommended): https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html

### Prerequisites
You will need the following libraries:

  •	pandas
  •	json
  •	random
  •	nltk
  •	itertools
  •	heapq

You will need the following files:

•	Uni-gram and bi-gram words to substitute with the most similar word(uni-gram) and insert the word that is most likely to follow(bi-gram):

•	c-06d to create a dictionary of phonemic models: http://www.greenteapress.com/thinkpython/code/c06d?fbclid=IwAR3kK8u0l48ksaGi8v60FZLDsSjpdjhw3dCCeZdRDS0VkBhgeR5YyzSUTuI


## Code
Code is broken down into the following files:

### 1.	Shared
•	Manual transcripts were in json format – use json.loads in store_tr(df) to store them
•	Function flatten(tr) flattens the stored transcript to do the word_count(fl_tr) to determine how many words need to be altered at a certain rate (0.2, 0.4, 0.6) and create a list of these words at random by random_words_list(fl_tr, rate)
•	create_one_gram_list() creates a list of uni-grams with the associated probability of this word to appear in text/speech. A reduced list of 2,000 most used words created for the transcript unigram dictionary in substitution file

### 2.	Deletion
•	Delete words from manual transcript that match those on the random_words_list(fl_tr, rate)
