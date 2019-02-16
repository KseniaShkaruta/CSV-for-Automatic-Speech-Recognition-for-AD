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
