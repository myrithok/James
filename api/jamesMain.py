#Project imports
from jamesClasses import jamesCorpus, jamesResults, docResults, inputCorpus
from jamesPreProcessing import preProcess, preProcessSentence
from jamesLDA import buildBestCoherenceTopicModel, buildTopicModel, getTopics, getResults
from jamesSA import loadSentimentModel, getSentenceSentiment
from jamesConfig import sentimentFilename

#Main method called by server.py to handle processing of input corpus
#Optional argument topicNum allows user to specify a number of topics for topic model if desired
#Input: an inputCorpus object (imported from jamesClasses) and an integer
#Output: a dictionary containing nested dictionaries, to be easily converted to a json object
def process(inputCorpus,topicNum=None):
	#Pre process input corpus using preProcess method imported from jamesPreProcessing
	#Input is inputCorpus object, imported from jamesClasses
	#Output is jamesCorpus object, imported from jamesClasses
	corpus = preProcess(inputCorpus)
	#If a specific number of topics is not specified, build a topic model for the
	#	preprocessed corpus using buildBestCoherenceTopicModel, imported from jamesLDA
	#This method finds a number of topics that produces the best average coherence
	#	score, and returns this topic model
	if topicNum == None:
		topicModel = buildBestCoherenceTopicModel(corpus)
	#If a number of topics is specified, simply build a topic model for the input corpus
	#	with the specified number of topics using buildTopicModel, imported from jamesLDA
	else:
		topicModel = buildTopicModel(corpus,topicNum)
	#Load the sentiment model using loadSentimentModel, imported from jamesSA
	sentimentModel = loadSentimentModel(sentimentFilename())
	#Produce a jamesResults object, imported from jamesClasses, containing the topic
	#	model information using getResults, imported from jamesLDA
	results = getResults(topicModel,corpus)
	#Add the stem dictionary produced in preprocessing to the jamesResults object
	#Words are stemmed for topic modeling, but a dictionary is kept mapping each stem
	#	to a word converted to that stem, which is used to make results more readable
	results.addStemDic(corpus.stemDic)
	#Iterate through each document in the corpus for analysis
	for doc in corpus.docs:
		#Construct a docResults object, imported from jamesClasses, containing the topic
		#	breakdown compared to the constructed topic model for the document in question
		#	produced by getTopics, imported from jamesLDA
		docResult = docResults(doc.title,getTopics(doc.bow,topicModel))
		#Iterate through each sentence in the document for sentiment analysis
		for sentence in doc.sentences:
			#Preprocess the sentence for topic modeling
			processedSentence = preProcessSentence(sentence,corpus.dic)
			#Use the constructed topic model to find the topic distribution for the
			#	current sentence using getTopics, imported from jamesLDA
			sentenceTopics = getTopics(processedSentence,topicModel)
			#Use the sentiment analysis model to find the sentiment for the current
			#	sentence using getSentenceSentiment, imported from jamesSA
			sentenceSentiment = getSentenceSentiment(sentence,sentimentModel)
			#Add the sentence's sentiment to each topic's sentiment for the current
			#	document results docResults object, weighted by the sentence's topic
			#	distribution
			for topic in sentenceTopics:
				docResult.addSentiment(topic[0],topic[1],sentenceSentiment)
		#Calculate the average sentiment for each topic in the current document
		docResult.averageSentiments()
		#Add the docResults object to the jamesResults result set
		results.addDocResults(docResult)
	#Use the jamesResults output method to output results as nested dictionaries
	#	and lists, which can be converted to a json object
	return results.output()