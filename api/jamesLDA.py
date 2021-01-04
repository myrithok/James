from jamesClasses import BoW, topicModel, resultTopicWord, resultTopic, jamesResults
from gensim.models import ldamodel

def buildTopicModel(document,topicNum=2):
	chunksize = 2000
	passes = 20
	iterations = 400
	eval_every = None
	ldaModel = ldamodel.LdaModel(corpus = document.bow,
								  num_topics=topicNum,
								  id2word=document.dic,
								  chunksize=chunksize,
								  alpha='auto',
								  eta='auto',
								  iterations=iterations,
								  passes=passes,
								  eval_every=eval_every)
	return topicModel(ldaModel,document)

def getResults(topicModel):
	return jamesResults(topicModel.model.top_topics(topicModel.document.bow))

def getSentenceTopics(sentence, topicModel):
	return topicModel.model.get_document_topics(sentence.bow,0.0)[0]

#TODO: Used up to here

def topicModelBestCoherence(processed,maximum):
	topicNum = bestCoherence(processed,maximum)
	return topicModel(processed,topicNum)

def bestCoherence(processed,maximum):
	scores = []
	for n in range(2,maximum):
		m = topicModel(processed,n)
		s = averageCoherence(m,processed)
		scores.append(s)
	return scores.index(max(scores)) + 2

def averageCoherence(model,processed):
	return (sum([t[1] for t in model.top_topics(processed.bow)]) / len(model.top_topics(processed.bow)))