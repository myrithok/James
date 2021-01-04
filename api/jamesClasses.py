class BoW:
	def __init__(self,bow,dic):
		self.bow = bow
		self.dic = dic

class resultTopicWord:
	def __init__(self,raw):
		self.weight = raw[0]
		self.stem = raw[1]
	def print(self):
		output = self.stem
		output += ":"
		output += str(self.weight)
		return output

class resultTopic:
	def __init__(self,raw):
		self.coherence = raw[1]
		self.words = []
		for word in raw[0]:
			self.words.append(resultTopicWord(word))
		self.sentimentSum = 0
		self.sentimentNum = 0
	def addSentiment(self,value):
		self.sentimentSum += value
		self.sentimentNum += 1
	def getSentiment(self):
		if self.sentimentNum == 0:
			return 0
		return self.sentimentSum / self.sentimentNum

class jamesResults:
	def __init__(self,raw):
		self.topics = []
		for topic in raw:
			self.topics.append(resultTopic(topic))
	def addSentiment(self,topicNum,value):
		self.topics[topicNum].addSentiment(value)
	def output(self):
		output = ""
		i = 1
		for topic in self.topics:
			output += "Topic "
			output += str(i)
			output += "\n"
			output += "Sentiment: "
			output += str(topic.getSentiment())
			output += "\n"
			output += "Coherence: "
			output += str(topic.coherence)
			output += "\n"
			output += "Words: \n"
			for word in topic.words:
				output += word.print()
				output += ", "
			output = output[:-2]
			output += "\n\n"
			i += 1
		return output

class topicModel:
	def __init__(self,model,document):
		self.model = model
		self.document = document