# The jamesResults class is used to represent the result set of this application
# It has 3 properties:
#	topicResults: a list of topic results as topicResults objects (found below)
#	stemDic: a dictionary mapping word stems to an example of a corresponding word
#	documentResults: a list of results corresponding to each document
class jamesResults:
    # jamesResults is initialized with the results of a topic model
    # The topic results are loaded into the topicResults property, and
    #	the other two properties are initialized as empty
    # Input: the results of the top_topics method of a gensim ldamodel
    def __init__(self, topicOutput):
        self.topicResults = []
        self.stemDic = {}
        self.documentResults = []
        i = 1
        for result in topicOutput:
            self.topicResults.append(topicResults(i, result))
            i += 1

    # This method is used to add the results of a single document to the
    #	documentResults property
    # Input: a docResults object, found below
    def addDocResults(self, docResults):
        self.documentResults.append(docResults)

    # This method is used to load a stem dictionary into the stemDic property
    # Input: a dictionary mapping word stems to an example of a word that
    #	produces that stem
    def addStemDic(self, stemDic):
        self.stemDic = stemDic

    # This method is used to get the number of topics in the result set
    # Output: the number of topics in the topic results as an integer
    def getNumberOfTopics(self):
        return len(self.topicResults)

    # This method is used to recursively construct the entire object and
    #	all nested objects into nested dictionaries and lists which can be
    #	easily converted to a json object
    # This is used to format the results into a response once the result set
    #	is complete
    def output(self):
        topicsOut = []
        documentsOut = []
        for topic in self.topicResults:
            topicsOut.append(topic.output(self.stemDic))
        for document in self.documentResults:
            documentsOut.append(document.output())
        return {"topics": topicsOut,
                "sentiments": documentsOut}


# The topicResults class is used to represent the results for a single topic
# The topicResults propety of the jamesResults class is a list of these
# It has 3 proprties:
#	topicNum: the identifying number of this topic (e.g. topic 1, topic 2, etc)
#	coherence: the coherence score for this topic
#	topicWords: a list of words and their corresponding weights, which represent
#				the meaning of the topic, as topicWord objects (found below)
class topicResults:
    # topicResults is initialized with the results of a single topic form the
    #	output of the gensim ldamodel top_topics method
    # Input: an integer denoting the number of the topic, and (word list, coherence) pair,
    #	where the coherence is a float and the word list is a list of (float, string) pairs
    def __init__(self, num, result):
        self.topicNum = num
        self.coherence = result[1]
        self.topicWords = []
        for word in result[0]:
            self.topicWords.append(topicWord(word))

    # This method is used to recursively construct the object and all nested
    #	objects into nested dictionaries and lists which can be easily
    #	converted to a json object
    # This is used to format the results into a response once the result set
    #	is complete
    def output(self, stemDic):
        wordsOut = []
        for word in self.topicWords:
            wordsOut.append(word.output(stemDic))
        return {"topicnum": self.topicNum,
                "coherence": str(self.coherence),
                "topicwords": wordsOut}


# The topicWord class is used to represent a single word and its corresponding weight
#	in the result set of a single topic
# The topicWords propety of the topicResults class is a list of these
# It has 2 properties:
#	word: the word as a string
#	weight: the weight of this word
class topicWord:
    # topidWord is initialized with a (weight,word) pair
    # Input: a (weight,word) pair, where the word is a string and the weight
    #	is a float
    def __init__(self, word):
        self.word = word[1]
        self.weight = word[0]

    # This method is used to  construct the object into a dictionary which can
    #	be easily converted to a json object
    # This is used to format the results into a response once the result set
    #	is complete
    def output(self, stemDic):
        return {"word": stemDic[self.word],
                "weight": str(self.weight)}


# The docResults class is used to represent the results of analyzing a
#	single document
# The documentResults propety of the jamesResults class is a list of these
# It has 2 properties:
#	docTitle: the title of the document, as a string
#	docTopics: a list topic results for the document, as docTopic
#				objects (found below)
class docResults:
    # docResults is initialized with the title of the document, and the topic
    #	distribution for the document
    # Input: the title of the document as a string, and a list of
    #	(topic number, weight) pairs where the topic number is an integer
    #	and the weight is a float
    def __init__(self, title, topics):
        self.docTitle = title
        self.docTopics = []
        for topic in topics:
            self.docTopics.append(docTopic(topic))

    # This method is used to add sentiment weight to specific topic in the
    #	document results
    # Input: the topic number to add sentiment to as an integer, and the
    #	sentiment weight to be added as a float
    def addSentiment(self, num, weight, sentiment):
        self.docTopics[num - 1].addSentiment(weight, sentiment)

    # This method is used to average the sentiment weight of each topic once
    #	all sentiment has been added
    def averageSentiments(self):
        for topic in self.docTopics:
            topic.averageSentiments()

    # This method is used to recursively construct the object and all nested
    #	objects into nested dictionaries and lists which can be easily
    #	converted to a json object
    # This is used to format the results into a response once the result set
    #	is complete
    def output(self):
        topicsOut = []
        for topic in self.docTopics:
            topicsOut.append(topic.output())
        return {"doctitle": self.docTitle,
                "topics": topicsOut}


# The docTopic class is used to represent the results of a single topic for
#	a single document
# The docTopics property of the docResults class is a list of these
# It has 4 properties:
#	topicNum: an integer corresponding to the number of the topic
#	weight: a float corresponding to the weight of the topic in the document
#	sentimentTotal: a float corresponding to the document's sentiment towards
#					that topic
#	sentimentWeight: a float corresponding to the total sentence weight that
#						has been contributed to the topic, used for averaging
class docTopic:
    # docTopic is initialized with the weight of a single topic for a single document,
    #	and sentiment and sentences are both initialized to 0
    # Input: a (topic number, weight) pair, where the topic number is an integer and
    #	the weight is a float
    def __init__(self, topic):
        self.topicNum = topic[0] + 1
        self.weight = topic[1]
        self.sentimentTotal = 0.0
        self.sentimentWeight = 0.0

    # This method is used to add the sentiment weighting of a single sentence
    # It adds the sentiment multiplied by the sentence weight to the sentiment total,
    #	and the sentence weight to the sentence weight total
    # Input: a sentence weight as a float, and a sentence sentiment as a float
    def addSentiment(self, weight, sentiment):
        self.sentimentTotal += sentiment * weight
        self.sentimentWeight += weight

    # This method is used to average the sentiment of the topic by dividing the total
    #	sentiment by the total weight of sentences added
    def averageSentiments(self):
        self.sentimentTotal = self.sentimentTotal / self.sentimentWeight

    # This method is used to  construct the object into a dictionary which can
    #	be easily converted to a json object
    # This is used to format the results into a response once the result set
    #	is complete
    def output(self):
        return {"topicnum": self.topicNum,
                "weight": str(self.weight),
                "sentiment": str(self.sentimentTotal)}


# The inputCorpus class is used to represent a corpus input being read from
#	input files
# This information of this class is only used until it can be preprocessed into
#	a jamesCorpus object (found below)
# It has 1 propety:
#	docs: a list of document information, represented as corpusDoc objects (found below)
class inputCorpus:
    # inputCorpus is initialized with an empty document list
    def __init__(self):
        self.docs = []

    # This method is used to add a document as a corpusDoc object (found below)
    #	to the inputCorpus object
    # Input: the document's title as a string, and the document contents as a string
    def addDoc(self, title, doc):
        self.docs.append(corpusDoc(title, doc))


# The jamesCorpus class is used to represent a preprocessed corpus, with all
#	necessary information 
# It has 3 properties:
#	docs: a list of corpusDoc objects representing the preprocessed documents
#	dic: a gensim Dictionary mapping word ids to word stems, needed for topic modeling
#	stemDic: a dictionary mapping word stems to an example of a word that produced
#				this stem
class jamesCorpus:
    # jamesCorpus is initialized with values for all 3 properties
    # Input: a list of corpusDoc objects, a word id stem dictionary as a gensim Dictionary
    #	where the keys are integers and the values are strings, and a stem word dictionary
    #	where the keys and values are strings
    def __init__(self, docs, dic, stemDic):
        self.docs = docs
        self.dic = dic
        self.stemDic = stemDic

    # This method is used to get a list of bags of words, where each bag of words is
    #	corresponds to one document in the corpus
    # Output: a bag of words as a list of (integer, integer) pairs
    def getBoW(self):
        bow = []
        for doc in self.docs:
            bow.append(doc.bow)
        return bow


# The corpusDoc class is used to represent a single document within a corpus
# The docs propety of the inputCorpus class and the docs propety of the jamesCorpus
#	class are both lists of these
# It has 5 properties:
#	title: the title of the document as a string
#	text: the text of the document as a string
#	lemmatized: the text of the document in lemmatized form, as a list of strings
#	bow: the text of the document in bag of words form, as a list of
#			(integer, integer) pairs
#	sentences: the text of the document separated into a list of sentences, where
#				each sentence is a string
class corpusDoc:
    # corpusDoc is initialized with just the title and text of the document
    # The other 3 properites are initialized to empty lists
    # Input: the title of the document as a string, and the text of the
    #	document as a string
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.lemmatized = []
        self.bow = []
        self.sentences = []

    # This method is used to add the text of the document in lemmatized form
    #	after preprocesing
    # Input: the text of the document in lemmatized form as a list of strings
    def addLemmatized(self, lemmatized):
        self.lemmatized = lemmatized

    # This method is used to add the text of the document in bag of words form
    #	after preprocessing
    # Input: the text of the document in bag of words form, as a list of
    #	(integer, integer) pairs
    def addBoW(self, bow):
        self.bow = bow

    # This method is used to add a list of sentences in the document
    # Input: the text of the document separated into a list of sentences, where
    #	each sentence is a string
    def addSentences(self, sentences):
        self.sentences = sentences
