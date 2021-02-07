# Library imports
import os
import sys
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

class jamesResults:
    '''
    The jamesResults class is used to represent the result set of this application

    Attributes
    ----------
            topicResults: list
                    a list of topic results as topicResults objects (found below)

            stemDic: dict
                    a dictionary mapping word stems to an example of a corresponding word

            documentResults: list
                    a list of results corresponding to each document

    Methods
    --------
            addDocResults(docResults: docResults)
                    used to add the results of a single document to the
                    documentResults property

            addStemDic(stemDic: dict)
                    used to load a stem dictionary into the stemDic property

            getNumberOfTopics() -> int
                    get the number of topics in the result set

            output() -> dict
                    This method is used to recursively construct the entire object and
                    all nested objects into nested dictionaries and lists which can be
                    easily converted to a json object
    '''

    def __init__(self, topicOutput):
        '''
        jamesResults objects are initialized with the results of a topic model

        Parameters
        ----------
                topicOutput: list
                        the results of the top_topics method of a gensim ldamodel
        '''
        if not topicOutput:
            raise Exception("Empty input value")
        self.topicResults = []
        self.stemDic = {}
        self.documentResults = []
        i = 1
        for result in topicOutput:
            self.topicResults.append(topicResults(i, result))
            i += 1

    def addDocResults(self, docResults):
        '''
        Parameters
        ----------
                docResults: docResults
                        the results for a single document as a docResults 
                        object, found below
        '''
        self.documentResults.append(docResults)

    def addStemDic(self, stemDic):
        '''
        Parameters
        ----------
                stemDic: dict
                        a dictionary mapping word stems to an example of a word
                        that produces that stem
        '''
        self.stemDic = stemDic

    def getNumberOfTopics(self):
        '''
        Output
        ------
                int
                        the number of topics in the topic results as an integer
        '''
        return len(self.topicResults)

    def output(self):
        '''
        Output
        ------
                dict
                        the entire results set formatted as a dictionary
        '''
        topicsOut = []
        documentsOut = []
        for topic in self.topicResults:
            topicsOut.append(topic.output(self.stemDic))
        for document in self.documentResults:
            documentsOut.append(document.output())
        return {"topics": topicsOut,
                "sentiments": documentsOut}

class topicResults:
    '''
    The topicResults class is used to represent the results for a single topic

    Attributes
    ----------
            topicNum: int
                    the identifying number of this topic (e.g. topic 1, topic 2, etc)

            coherence: float
                    the coherence score for this topic

            topicWords: list
                    a list of words and their corresponding weights, which represent
                    the meaning of the topic, as topicWord objects (found below)

    Methods
    -------
            output(stemDic: dict) -> dict
                    This method is used to recursively construct the object and all nested
                    objects into nested dictionaries and lists which can be easily
                    converted to a json object
    '''
    def __init__(self, num, result):
        '''
        topicResults is initialized with the results of a single topic form the
        output of the gensim ldamodel top_topics method

        Parameters
        ----------
                num: int
                        an integer denoting the number of the topic, and (word list, coherence pair),
                        where the coherence is a float and the word list is a list of (float, string) pairs

        Methods
        -------
                output(stemDic: dict) -> dict
                        This method is used to recursively construct the object and all nested
                        objects into nested dictionaries and lists which can be easily
                        converted to a json object
        '''
        self.topicNum = num
        self.coherence = result[1]
        self.topicWords = []
        for word in result[0]:
            self.topicWords.append(topicWord(word))

    def output(self, stemDic):
        '''
        Parameters
        ----------
                stemDic: dict
                        a dictionary mapping word stems to an example of a word
                        that produces that stem

        Output
        ------
                dict
                        the topic results formatted as a dictionary
        '''
        wordsOut = []
        for word in self.topicWords:
            wordsOut.append(word.output(stemDic))
        return {"topicnum": self.topicNum,
                "coherence": str(self.coherence),
                "topicwords": wordsOut}

class topicWord:
    '''
    The topicWord class is used to represent a single word and its corresponding weight
    in the result set of a single topic

    Attributes
    ----------
            word: str
                the word as a string

            weight: float
                the weight of this word

    Methods
    -------
            output(stemDic: dict) -> dict
                    This method is used to  construct the object into a dictionary which can
                    be easily converted to a json object
    '''
    def __init__(self, word):
        '''
        topicWord is initialized with a (weight,word) pair

        Parameters
        ----------
                word: tuple
                        a (weight,word) pair, where the word is a string and the weight
                        is a float
        '''
        self.word = word[1]
        self.weight = word[0]

    def output(self, stemDic):
        '''
        Parameters
        ----------
                stemDic: dict
                        a dictionary mapping word stems to an example of a word
                        that produces that stem

        Output
        ------
                dict
                        the word data formatted as a dictionary
        '''
        return {"word": stemDic[self.word],
                "weight": str(self.weight)}

class docResults:
    '''
    The docResults class is used to represent the results of analyzing a
    single document

    Attributes
    ----------
            docTitle: str
                    the title of the document, as a string

            docTopics: list
                    a list topic results for the document, as docTopic
                    objects (found below)

    Methods
    -------
            addSentiment(num: int, weight: float, sentiment: float)
                    This method is used to add sentiment weight to specific topic in the
                    document results

            averageSentiment()
                    This method is used to average the sentiment weight of each topic once
                    all sentiment has been added

            output() -> dict
                    This method is used to recursively construct the object and all nested
                    objects into nested dictionaries and lists which can be easily
                    converted to a json object
    '''
    def __init__(self, title, topics):
        '''
        docResults is initialized with the title of the document, and the topic
        distribution for the document

        Parameters
        ----------
                title: str
                        the title of the document as a string

                topics: list
                        a list of (topic number, weight) pairs where the topic number is an integer
                        and the weight is a float
        '''
        self.docTitle = title
        self.docTopics = []
        for topic in topics:
            self.docTopics.append(docTopic(topic))

    def addSentiment(self, num, weight, sentiment):
        '''
        Parameters
        ----------
                num: int
                        the topic number to add sentiment to as an integer

                weight: float
                        the sentiment weight to be added as a float

                sentiment: float
                        the sentiment for a given topic
        '''
        self.docTopics[num-1].addSentiment(weight, sentiment)

    def averageSentiments(self):
        '''
        Find the average sentiment for each topic
        '''
        for topic in self.docTopics:
            topic.averageSentiments()

    def output(self):
        '''
        Output
        ------
                dict
                        the document results formatted as a dictionary
        '''
        topicsOut = []
        for topic in self.docTopics:
            topicsOut.append(topic.output())
        return {"doctitle": self.docTitle,
                "topics": topicsOut}

class docTopic:
    '''
    The docTopic class is used to represent the results of a single topic for
    a single document

    Attributes
    ----------
            topicNum: int
                    an integer corresponding to the number of the topic

            weight: float
                    a float corresponding to the weight of the topic in the document

            sentimentTotal: float
                    a float corresponding to the document's sentiment towards
                    that topic

            sentimentWeight: float
                    a float corresponding to the total sentence weight that
                    has been contributed to the topic, used for averaging

    Methods
    -------
            addSentiment(weight: float, sentiment: float)
                    This method is used to add the sentiment weighting of a single sentence
                    It adds the sentiment multiplied by the sentence weight to the sentiment total,
                    and the sentence weight to the sentence weight total

            averageSentiments()
                    This method is used to average the sentiment of the topic by dividing the total
                    sentiment by the total weight of sentences added

            output() -> dict
                    This method is used to  construct the object into a dictionary which can
                    be easily converted to a json object
    '''
    def __init__(self, topic):
        '''
        docTopic is initialized with the weight of a single topic for a single document,
        and sentiment and sentences are both initialized to 0

        Parameters
        ----------
                topic: tuple
                        a (topic number, weight) pair, where the topic number is an integer and
                        the weight is a float
        '''
        self.topicNum = topic[0] + 1
        self.weight = topic[1]
        self.sentimentTotal = 0.0
        self.sentimentWeight = 0.0

    def addSentiment(self, weight, sentiment):
        '''
        Parameters
        ----------
                weight: float
                        a sentence weight as a float

                sentiment: float
                        a sentence sentiment as a float
        '''
        self.sentimentTotal += sentiment * weight
        self.sentimentWeight += weight

    def averageSentiments(self):
        '''
        Average the sentiment for this topic by dividing it by the total topic weight added
        '''
        self.sentimentTotal = self.sentimentTotal / self.sentimentWeight

    def output(self):
        '''
        Output
        ------
                dict
                        the topic data for a single document formatted as a dictionary
        '''
        return {"topicnum": self.topicNum,
                "weight": str(self.weight),
                "sentiment": str(self.sentimentTotal)}

class inputCorpus:
    '''
    The inputCorpus class is used to represent a corpus input being read from
    input files. This information of this class is only used until it can be
    preprocessed into a jamesCorpus object (found below).

    Attributes
    ----------
            docs: list
                    a list of document information, represented as corpusDoc objects (found below)

    Methods
    -------
            addDoc(title: str, doc: str)
                    This method is used to add a document as a corpusDoc object (found below)
                    to the inputCorpus object
    '''
    def __init__(self):
        self.docs = []

    def addDoc(self, title, doc):
        '''
        Parameters
        ----------
        title: str
                the document's title as a string

        doc: str
                the document contents as a string
        '''
        self.docs.append(corpusDoc(title, doc))

class jamesCorpus:
    '''
    The jamesCorpus class is used to represent a preprocessed corpus, with all
    necessary information

    Attributes
    ----------
            docs: list
                    a list of corpusDoc objects representing the preprocessed documents

            dic: gensim.corpora.Dictionary
                    a gensim Dictionary mapping word ids to word stems, needed for topic modeling

            stemDic: dict
                    a dictionary mapping word stems to an example of a word that produced
                    this stem

    Methods
    -------
            getBoW() -> list
                    This method is used to get a list of bags of words, where each bag of words is
                    corresponds to one document in the corpus

            getLemmatized() -> list
                    This method is used to get a list of lists of strings, where each list corresponds
                    to one document in the corpus
    '''
    def __init__(self, docs, dic, stemDic):
        '''
        Parameters
        ----------
                docs: list
                        a list of corpusDoc objects

                dic: gensim.corpora.Dictionary
                        a word id stem dictionary as a gensim Dictionary
                        where the keys are integers and the values are strings

                stemDic: dict
                        a stem word dictionary
                        where the keys and values are strings
        '''
        self.docs = docs
        self.dic = dic
        self.stemDic = stemDic

    def getBoW(self):
        '''
        Output
        ------
                list
                        a bag of words as a list of (integer, integer) pairs
        '''
        bow = []
        for doc in self.docs:
            bow.append(doc.bow)
        return bow

    def getLemmatized(self):
        '''
        Output
        ------
                list
                        a bag of words as a list of lists of strings
        '''
        lemma = []
        for doc in self.docs:
            lemma.append(doc.lemmatized)
        return lemma

class corpusDoc:
    '''
    The corpusDoc class is used to represent a single document within a corpus
    The docs property of the inputCorpus class and the docs property of the jamesCorpus
    class are both lists of these

    Attributes
    ----------
            title: str
                    the title of the document as a string

            text: str
                    the text of the document as a string

            lemmatized: list
                    the text of the document in lemmatized form, as a list of strings

            bow: list
                    the text of the document in bag of words form, as a list of (integer, integer) pairs

            sentences: list
                    the text of the document separated into a list of sentences, where
                    each sentence is a string

    Methods
    -------
            addLemmatized(lemmatized: list)
                    This method is used to add the text of the document in lemmatized form
                    after preprocesing

            addBoW(bow: list)
                    This method is used to add the text of the document in bag of words form
                    after preprocessing

            addSentences(sentences: list)
                    This method is used to add a list of sentences in the document
    '''
    def __init__(self, title, text):
        '''
        corpusDoc is initialized with just the title and text of the document
        The other 3 attributes are initialized to empty lists

        Parameters
        ----------
                title: str
                        the title of the document as a string

                text: str
                        the text of the document as a string
        '''
        self.title = title
        self.text = text
        self.lemmatized = []
        self.bow = []
        self.sentences = []

    def addLemmatized(self, lemmatized):
        '''
        Parameters
        ----------
                lemmatized: list
                        the text of the document in lemmatized form as a list of strings
        '''
        self.lemmatized = lemmatized

    def addBoW(self, bow):
        '''
        Parameters
        ----------
                bow: list
                        the text of the document in bag of words form, as a list of
                        (integer, integer) pairs
        '''
        self.bow = bow

    def addSentences(self, sentences):
        '''
        Parameters
        ----------
                sentences: list
                        the text of the document separated into a list of sentences, where
                        each sentence is a string
        '''
        self.sentences = sentences
