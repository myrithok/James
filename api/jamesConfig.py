#This file is meant to gather hard-coded names or values in one place
#sentimentFilename is the name of the saved sentiment analysis model 
#This is used to save and load the model by jamesSA
def sentimentFilename():
	return "jamesSentimentModel.pickle"
#jamesTMSettings provides a dictionary of settings for the LDA topic model
#It is used by jamesLDA
def jamesTMSettings():
	return {'chunkSize':2000,
			'alpha':'auto',
			'eta':'auto',
			'passes':1,
			'iterations':50,
			'evalEvery':None}
#jamesTopicMaximum provides the maximum number of topics to test when testing
#	for the number of topics that produces the highest average coherence score
#It is used by jamesLDA
def jamesTopicMaximum():
	return 20
#jamesTrainingData provides the training data source for the sentiment analysis model
def jamesTrainingData():
	from nltk.corpus import twitter_samples
	return {"Positive":twitter_samples.tokenized('positive_tweets.json'),
			"Negative":twitter_samples.tokenized('negative_tweets.json')}