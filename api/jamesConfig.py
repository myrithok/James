#This file is meant to gather hard-coded names or values in one place
#sentimentFilename is the name of the saved sentiment analysis model 
#This is used to save and load the model by jamesSA
def sentimentFilename():
	return "jamesSentimentModel.pickle"
#jamesChunkSize, jamesPasses, jamesIterations, and jamesEvalEvery are
#	all parameters for building a topic model
#They are used by jamesLDA
def jamesChunkSize():
	return 2000
def jamesPasses():
	return 1
def jamesIterations():
	return 50
def jamesEvalEvery():
	return None
#jamesTrainingData provides the training data source for the sentiment analysis model
def jamesTrainingData():
	from nltk.corpus import twitter_samples
	return {"Positive":twitter_samples.tokenized('positive_tweets.json'),
			"Negative":twitter_samples.tokenized('negative_tweets.json')}