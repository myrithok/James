from jamesClasses import jamesCorpus, jamesResults, docResults, inputCorpus
from jamesPreProcessing import preProcess, preProcessSentence
from jamesLDA import buildBestCoherenceTopicModel, buildTopicModel, getTopics, getResults
from jamesSA import loadSentimentModel, getSentenceSentiment

def process(corpus,topicNum=None):
	corpus = preProcess(corpus)
	if topicNum == None:
		topicModel = buildBestCoherenceTopicModel(corpus)
	else:
		topicModel = buildTopicModel(corpus,topicNum)
	sentimentModel = loadSentimentModel()
	results = getResults(topicModel,corpus)
	results.addStemDic(corpus.stemDic)
	for doc in corpus.docs:
		docResult = docResults(doc.title,getTopics(doc.bow,topicModel))
		for sentence in doc.sentences:
			processedSentence = preProcessSentence(sentence,corpus.dic)
			sentenceTopics = getTopics(processedSentence,topicModel)
			sentenceSentiment = getSentenceSentiment(sentence,sentimentModel)
			for topic in sentenceTopics:
				docResult.addSentiment(topic[0],topic[1]*sentenceSentiment)
		docResult.averageSentiments()
		results.addDocResults(docResult)
	return results.output()