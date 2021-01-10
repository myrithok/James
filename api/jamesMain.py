from jamesClasses import jamesCorpus, jamesResults, docResults, inputCorpus
from jamesPreProcessing import preProcess, preProcessSentence
from jamesLDA import buildTopicModel, getTopics, getResults
from jamesSA import loadSentimentModel, getSentenceSentiment

def process(corpus):
	corpus = preProcess(corpus)
	topicModel = buildTopicModel(corpus)
	sentimentModel = loadSentimentModel()
	results = getResults(topicModel,corpus)
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

def testProcess(a,b):
	f1 = open(a,"r")
	x = f1.read()
	f1.close()
	f2 = open(b,"r")
	y = f2.read()
	f2.close()
	data = inputCorpus()
	data.addDoc(a,x)
	data.addDoc(b,y)
	return process(data)

file1 = "netflix_chips.txt"
file2 = "macro_micro.txt"
testResults = testProcess(file1,file2)
print(testResults)