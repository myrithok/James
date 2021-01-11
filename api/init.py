#This script is used to prepare everything necessary for the James backend to run
#The intention is that this script is run only once on setup, and then again
#	only if something loaded by this file needs to change

#Library imports
import nltk
import numpy as np
import pickle
#Project imports
from jamesSA import buildSentimentModel
import jamesConfig

#The init method performs all necessary initialization
def init():
	#Set a seed, and load everything necessary from nltk
	np.random.seed(2018)
	nltk.download('wordnet')
	nltk.download('twitter_samples')
	nltk.download('punkt')
	nltk.download('averaged_perceptron_tagger')
	#Build the sentiment model using buildSentimentModel, imported from jamesSA
	sentimentModel = buildSentimentModel()
	#Save the sentiment model using pickle, to a filename imported from jamesConfig
	f = open(jamesConfig.sentimentFilename(),"wb")
	pickle.dump(sentimentModel,f)
	f.close()
	
#Run init
init()