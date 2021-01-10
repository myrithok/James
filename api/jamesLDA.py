from jamesClasses import jamesCorpus, jamesResults
from gensim.models import ldamodel

def buildTopicModel(corpus,topicNum):
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

def buildBestCoherenceTopicModel(corpus,maximum=20):
	topicNum = bestCoherence(corpus,maximum)
	return buildTopicModel(corpus,topicNum)

def bestCoherence(corpus,maximum):
	scores = []
	for n in range(2,maximum+1):
		m = buildTopicModel(corpus,n)
		s = averageCoherence(m,corpus)
		scores.append(s)
	return scores.index(max(scores)) + 2

def averageCoherence(model,corpus):
	results = model.top_topics(corpus.getBoW())
	return (sum([t[1] for t in results]) / len(results))