from jamesClasses import jamesCorpus, jamesResults
from gensim.models import ldamodel

def buildTopicModel(corpus,topicNum=5):
	chunksize = 2000
	passes = 1
	iterations = 50
	eval_every = None
	ldaModel = ldamodel.LdaModel(corpus = corpus.getBoW(),
								  num_topics=topicNum,
								  id2word=corpus.dic,
								  chunksize=chunksize,
								  alpha='auto',
								  eta='auto',
								  iterations=iterations,
								  passes=passes,
								  eval_every=eval_every)
	return ldaModel

def getResults(topicModel,corpus):
	return jamesResults(topicModel.top_topics(corpus.getBoW()))

def getTopics(bow, topicModel):
	return topicModel.get_document_topics(bow,0.0)

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