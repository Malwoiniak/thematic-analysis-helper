#import necessary modules, libraries
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import Word2Vec, LdaMulticore
from IPython.display import HTML

from gensim.corpora import Dictionary

import numpy as np 
import pandas as pd
import glob
import pyLDAvis
from pyLDAvis import gensim 

from textblob import TextBlob

def preprocessing(sentence):
    """ Converts a document into a list of lowercase tokens, ignoring tokens that are too short or too long and stopwords."""
    return [word for word in simple_preprocess(sentence) \
            if word not in STOPWORDS]

def read_sentences(filename):
    """ Performs def preprocessing on given file one sentence (line) and the time"""
    with open(filename, 'rb') as f:
        for line in f:
            yield preprocessing(line)

if __name__ ==  '__main__':
	#Get list of preprocessed sentences for libdem.com (all years)
	sentences = list(read_sentences('libdem.txt'))

	#Get randomly permuted sentences 
	sentences_light = np.random.permutation(sentences)

	#Get 3000 of randomly permuted sentences
	sentences_light = sentences_light[:2500]

	#Get dictionary of normalized words and their ids 
	dictionary = Dictionary(sentences_light)

	#Convert doc into bag-of-words (BoW) for each sentence in sentences_light
	bow_corpus = [dictionary.doc2bow(sent) for sent in sentences_light]

	#train lda_model
	lda_model = LdaMulticore(bow_corpus, id2word=dictionary, num_topics=100, passes=20, workers=8)
	#Show topics, index in trained lda_model
	for idx, topic in lda_model.print_topics(-1):
		print('Topic: {}\nWords: {}'.format(idx, topic))

	#Visualize topics with pyLDAvis
	lda_vis = pyLDAvis.gensim.prepare(lda_model, bow_corpus, dictionary)
	pyLDAvis.show(lda_vis, local=False)