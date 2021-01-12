#This file is used exclusively for internally testing project methods
from jamesMain import process
from jamesClasses import jamesCorpus, jamesResults, docResults, inputCorpus
from jamesPreProcessing import preProcess, preProcessSentence
from jamesLDA import buildTopicModel, getTopics, getResults
from jamesSA import loadSentimentModel, getSentenceSentiment

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
	return process(data,3)

file1 = "netflix_chips.txt"
file2 = "macro_micro.txt"
testResults = testProcess(file1,file2)
print(testResults)