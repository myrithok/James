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