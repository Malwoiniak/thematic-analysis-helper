#import necessary modules, libraries
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import Word2Vec, LdaMulticore

from gensim.corpora import Dictionary

import numpy as np 
import pandas as pd
import glob
import pyLDAvis
from pyLDAvis import gensim 

from textblob import TextBlob

#Read data into DataFrame: concatenate scraped data from all years for jackbones.com
df = pd.concat([pd.read_csv(f) for f in glob.glob('neverseconds scrape/*.csv')])

#Get list of all sentences in summary content
content = ' '.join(df['summary'])
sentences = TextBlob(content).sentences
sent_list=[]
for s in sentences:
    sent_list.append(str(s))
    
#write all sentences to .txt  
with open('neverseconds.txt', 'w', encoding='utf-8') as f:
    for line in sent_list:
        f.write(line)
        f.write('\n')
f.close()

def preprocessing(sentence):
    """ Converts a document into a list of lowercase tokens, ignoring tokens that are too short or too long and stopwords."""
    return [word for word in simple_preprocess(sentence) \
            if word not in STOPWORDS]

def read_sentences(filename):
    """ Performs def preprocessing on given file one sentence (line) and the time"""
    with open(filename, 'rb') as f:
        for line in f:
            yield preprocessing(line)

#Get list of preprocessed sentences for jackbones.com (all years)
sentences = list(read_sentences('neverseconds.txt'))

#Train word2vec model (window, min_count: adjust if needed)
model = Word2Vec(sentences, window=1, min_count=3)        

#get list of synonyms in trained model
print('\nSynonyms of the word "good":\n', model.wv.most_similar('good'))
print()

#Perform mathematical operation on words: amazing+good-bad
print('Synonyms of mathematical operation on words "amazing+good-bad":\n',model.wv.most_similar(positive=['amazing', 'good'], negative=['bad']))
print()
#get list of synonyms in trained model
print('Synonyms of the word "bad":\n', model.wv.most_similar('bad'))
print()