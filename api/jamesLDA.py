#Library imports
from gensim.models import ldamodel
#Project imports
from jamesClasses import jamesCorpus, jamesResults
from jamesConfig import jamesTMSettings, jamesTopicMaximum

#This method is used to build a gensim topic model of the given number of 
#	topics for a given corpus
#Input: the corpus as a jamesCorpus object (imported from jamesClasses)
#	and the number of topics to generate
#Output: a gensim ldamodel
def buildTopicModel(corpus,topicNum):
	#Import the topic model settings from jamesConfig
	settings = jamesTMSettings()
	#Build the topic model using the given corpus, the given number
	#	of topics, and the given settings
	ldaModel = ldamodel.LdaModel(corpus = corpus.getBoW(),
								  num_topics=topicNum,
								  id2word=corpus.dic,
								  chunksize=settings['chunkSize'],
								  alpha=settings['alpha'],
								  eta=settings['eta'],
								  iterations=settings['iterations'],
								  passes=settings['passes'],
								  eval_every=settings['evalEvery'])
	#Return the topic model
	return ldaModel

#This method is used to the ideal number of topics for a topic model when
#	a number is not specified by the user
#This is done by building a topic model for each number of topics between 2 and
#	a maximum, then picking the topic model from these that had the highest average
#	coherence score for its topics
#Input: the corpus as a jamesCorpus object (imported from jamesClasses)
#Output: a gensim ldamodel
def buildBestCoherenceTopicModel(corpus):
	#Import the maximum number of topics to try from jamesConfig
	maximum = jamesTopicMaximum()
	#Initialize each variable to test the max
	topScore = topModel = currentModel = currentResults = currentScore = None
	#Iterate through each number of topics to try, between 2 and the maximum (inclusive)
	for n in range(2,maximum+1):
		#Build the topic model for the current number of topics using buildTopicModel found above
		currentModel = buildTopicModel(corpus,n)
		#Get the topic results for the built topic model
		currentResults = currentModel.top_topics(corpus.getBoW())
		#Find the average coherence score for the topics in the current model
		currentScore = (sum([t[1] for t in currentResults]) / len(currentResults))
		#If this model has a higher average coherence score than the current best,
		#	or it is the first model generated, store this model and score as the
		#	top model and score
		if topScore == None or currentScore > topScore:
			topScore = currentScore
			topModel = currentModel
	#Return the top model that was found
	return topModel

#This method is used to construct a jamesResults object (imported from jamesClasses)
#	containing the topic results of a given topic model and corpus
#Input: a gensim ldamodel and a jamesCorpus object (imported from jamesClasses)
#Output: a jamesResults object containing the results
def getResults(topicModel,corpus):
	return jamesResults(topicModel.top_topics(corpus.getBoW()))

#This method is used to find the topic distribution of a given document or sentence
#It is used by jamesMain to find the topic distribution of documents for the result set,
#	and to find the topic distribution of each sentence for sentiment weighting
#Input: a preprocessed bag of words to be checked against the topic model, and a gensim ldamodel
#Output: the topic distribution as a list of (topic number, weight) pairs, where the topic number
#	is an integer, and the weight is a float
def getTopics(bow, topicModel):
	return topicModel.get_document_topics(bow,0.0)