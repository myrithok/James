import nltk
import numpy as np
import pickle
from jamesSA import buildSentimentModel
import jamesConfig

def init():
	np.random.seed(2020)
	nltk.download('wordnet')
	nltk.download('twitter_samples')
	nltk.download('punkt')
	nltk.download('averaged_perceptron_tagger')
	sentimentModel = buildSentimentModel()
	f = open(jamesConfig.sentimentFilename(),"wb")
	pickle.dump(sentimentModel,f)
	f.close()

init()