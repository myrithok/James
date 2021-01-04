from jamesClasses import resultTopicWord, resultTopic, jamesResults, topicModel
from jamesPreProcessing import preProcess, separateSentences
from jamesLDA import buildTopicModel, getSentenceTopics, getResults
from jamesSA import loadSentimentModel, getSentenceSentiment

def process(data):
	processed = preProcess(data)
	sentences = separateSentences(data)
	topicModel = buildTopicModel(processed)
	sentimentModel = loadSentimentModel()
	results = getResults(topicModel)
	for sentence in sentences:
		processedSentence = preProcess(sentence)
		sentenceTopics = getSentenceTopics(processedSentence,topicModel)
		sentenceSentiment = getSentenceSentiment(sentence,sentimentModel)
		print(sentenceTopics)
		print(sentenceSentiment)
		for topic in sentenceTopics:
			results.addSentiment(topic[0],topic[1]*sentenceSentiment)
	return results.output()

def testProcess(filename):
	f = open(filename,"r")
	data = f.read()
	return process(data)

testFile = "canadian-covid_economy.txt"
testResults = testProcess(testFile)
print(testResults)