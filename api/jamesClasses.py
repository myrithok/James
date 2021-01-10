class jamesResults:
	def __init__(self,topicOutput):
		self.topicResults = []
		self.documentResults = []
		i = 1
		for result in topicOutput:
			self.topicResults.append(topicResults(i,result))
			i += 1
	def addDocResults(self,docResults):
		self.documentResults.append(docResults)
	def getNumberOfTopics(self):
		return len(self.topicResults)
	def output(self):
		topicsOut = []
		documentsOut = []
		for topic in self.topicResults:
			topicsOut.append(topic.output())
		for document in self.documentResults:
			documentsOut.append(document.output())
		return {"topics":topicsOut,
					"sentiments":documentsOut}

class topicResults:
	def __init__(self,num,result):
		self.topicNum = num
		self.coherence = result[1]
		self.topicWords = []
		for word in result[0]:
			self.topicWords.append(topicWord(word))
	def output(self):
		wordsOut = []
		for word in self.topicWords:
			wordsOut.append(word.output())
		return {"topicnum":self.topicNum,
				"coherence":str(self.coherence),
				"topicwords":wordsOut}

class topicWord:
	def __init__(self,word):
		self.word = word[1]
		self.weight = word[0]
	def output(self):
		return {"word":self.word,
				"weight":str(self.weight)}

class docResults:
	def __init__(self,title,topics):
		self.docTitle = ""
		self.docTopics = []
		for topic in topics:
			self.docTopics.append(docTopic(topic))
	def addSentiment(self,num,sentiment):
		self.docTopics[num-1].addSentiment(sentiment)
	def averageSentiments(self):
		for topic in self.docTopics:
			topic.averageSentiments()
	def output(self):
		topicsOut = []
		for topic in self.docTopics:
			topicsOut.append(topic.output())
		return {"doctitle":self.docTitle,
				"topics":topicsOut}

class docTopic:
	def __init__(self,topic):
		self.topicNum = topic[0]
		self.weight = topic[1]
		self.sentiment = 0.0
		self.sentences = 0
	def addSentiment(self,sentiment):
		self.sentiment += sentiment
		self.sentences += 1
	def averageSentiments(self):
		self.sentiment = self.sentiment / self.sentences
	def output(self):
		return {"topicnum":self.topicNum,
				"weight":str(self.weight),
				"sentiment":str(self.sentiment)}

class jamesCorpus:
	def __init__(self):
		self.docs = []
		self.dic = {}
	def __init__(self,docs,dic):
		self.docs = docs
		self.dic = dic
	def addDoc(self,title,doc):
		self.docs.append(corpusDoc(title,doc))
	def getBoW(self):
		bow = []
		for doc in self.docs:
			bow.append(doc.bow)
		return bow

class corpusDoc:
	def __init__(self,title,text):
		self.title = title
		self.text = text
		self.lemmatized = []
		self.bow = []
		self.sentences = []
	def addLemmatized(self,lemmatized):
		self.lemmatized = lemmatized
	def addBoW(self,bow):
		self.bow = bow
	def addSentences(self,sentences):
		self.sentences = sentences

class inputCorpus:
	def __init__(self):
		self.docs = []
	def addDoc(self,title,doc):
		self.docs.append(corpusDoc(title,doc))