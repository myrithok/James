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

            getNumberOfTopics()
                    get the number of topics in the result set

            output()
                    This method is used to recursively construct the entire object and
                    all nested objects into nested dictionaries and lists which can be
                    easily converted to a json object


    '''

    def __init__(self, topicOutput):
        '''
        Initialized with the results of a topic model

        Parameters
        ----------
                topicOutput:
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
                docResults:
                                a docResults object, found below

        '''
        self.documentResults.append(docResults)

    def addStemDic(self, stemDic):
        '''
        Parameters
        ----------
                stemDic: a dictionary mapping word stems to an example of a word
                        that produces that stem

        '''
        self.stemDic = stemDic

    def getNumberOfTopics(self):
        '''
        Output
        ------
                the number of topics in the topic results as an integer

        '''
        return len(self.topicResults)

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


class topicResults:
    '''
    The topicResults class is used to represent the results for a single topic

    Attributes
    ----------
            topicNum:
                    the identifying number of this topic (e.g. topic 1, topic 2, etc)
            coherence:
                    the coherence score for this topic
            topicWords:
                    a list of words and their corresponding weights, which represent
                    the meaning of the topic, as topicWord objects (found below)

    Methods
    -------
            output(stemDic):
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
                        num:
                                an integer denoting the number of the topic, and (word list, coherence pair),
                                where the coherence is a float and the word list is a list of (float, string) pairs

        Methods
        -------
                        output(stemDic):
                                        This method is used to recursively construct the object and all nested
                                        objects into nested dictionaries and lists which can be easily
                                        converted to a json object


        '''
        self.topicNum = num
        self.coherence = result[1]
        self.topicWords = []
        for word in result[0]:
            self.topicWords.append(topicWord(word))

    # This is used to format the results into a response once the result set
    #	is complete
    def output(self, stemDic):
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
            word:
                the word as a string

            weight:
                the weight of this word

    Methods
    -------
            output:
                                This method is used to  construct the object into a dictionary which can
                be easily converted to a json object


    '''

    def __init__(self, word):
        '''
        topicWord is initialized with a (weight,word) pair

        Parameters
        ----------
                word :
                a (weight,word) pair, where the word is a string and the weight
                        is a float

        '''
        self.word = word[1]
        self.weight = word[0]

    # This is used to format the results into a response once the result set
    #	is complete
    def output(self, stemDic):
        return {"word": stemDic[self.word],
                "weight": str(self.weight)}


class docResults:
    '''
    The docResults class is used to represent the results of analyzing a
    single document

    Attributes
    ----------
            docTitle:
                the title of the document, as a string

            docTopics:
                                a list topic results for the document, as docTopic
                                objects (found below)

    Methods
    -------
            addSentiment(num,weight,sentiment):
                    This method is used to add sentiment weight to specific topic in the
                    document results

            averageSentiment():
                                This method is used to average the sentiment weight of each topic once
                                all sentiment has been added


            output():
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
                        title:
                                the title of the document as a string

                topics:
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
                        num:
                                the topic number to add sentiment to as an integer

                        weight:
                                the sentiment weight to be added as a float

                        sentiment:
                                the sentiment for a given topic
        '''
        self.docTopics[num-1].addSentiment(weight, sentiment)

    def averageSentiments(self):
        for topic in self.docTopics:
            topic.averageSentiments()

    # This is used to format the results into a response once the result set
    #	is complete
    def output(self):
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
            topicNum:
                    an integer corresponding to the number of the topic

            weight:
                    a float corresponding to the weight of the topic in the document

            sentimentTotal:
                    a float corresponding to the document's sentiment towards
                    that topic

            sentimentWeight:
                    a float corresponding to the total sentence weight that
                    has been contributed to the topic, used for averaging

    Methods
    -------
            addSentiment(weight, sentiment):
                    This method is used to add the sentiment weighting of a single sentence
                    It adds the sentiment multiplied by the sentence weight to the sentiment total,
                    and the sentence weight to the sentence weight total

            averageSentiments():
                    This method is used to average the sentiment of the topic by dividing the total
                    sentiment by the total weight of sentences added

            output():
                    This method is used to  construct the object into a dictionary which can
                    be easily converted to a json object


    '''

    def __init__(self, topic):
        '''
        docTopic is initialized with the weight of a single topic for a single document,
and sentiment and sentences are both initialized to 0

        Parameters
        ----------
                topic:
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
                weight:
                        a sentence weight as a float

                sentiment:
                        a sentence sentiment as a float

        '''
        self.sentimentTotal += sentiment * weight
        self.sentimentWeight += weight

    def averageSentiments(self):
        self.sentimentTotal = self.sentimentTotal / self.sentimentWeight

    # This is used to format the results into a response once the result set
    #	is complete
    def output(self):
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
            docs:
                    a list of document information, represented as corpusDoc objects (found below)

    Methods
    -------
            addDoc:
                    This method is used to add a document as a corpusDoc object (found below)
                    to the inputCorpus object


    '''

    def __init__(self):
        self.docs = []

    def addDoc(self, title: str, doc: str):
        '''
        Parameters
        ----------
        title:
        the document's title as a string

        doc:
        the document contents as a string
        '''
        self.docs.append(corpusDoc(title, doc))


class jamesCorpus:
    '''
    The jamesCorpus class is used to represent a preprocessed corpus, with all
    necessary information

    Attributes
    ----------
            docs:
                    a list of corpusDoc objects representing the preprocessed documents

            dic:
                    a gensim Dictionary mapping word ids to word stems, needed for topic modeling

            stemDic:
                    a dictionary mapping word stems to an example of a word that produced
                    this stem


    Methods
    -------
            getBoW():
                    This method is used to get a list of bags of words, where each bag of words is
                    corresponds to one document in the corpus

    '''

    def __init__(self, docs, dic, stemDic):
        '''
        Parameters
        ----------
                docs:
                        a list of corpusDoc objects

                dic:
                        a word id stem dictionary as a gensim Dictionary
                        where the keys are integers and the values are strings

                stemDic:
                        a stem word dictionary
                        where the keys and values are strings



        '''
        self.docs = docs
        self.dic = dic
        self.stemDic = stemDic

    # Output: a bag of words as a list of (integer, integer) pairs
    def getBoW(self):
        bow = []
        for doc in self.docs:
            bow.append(doc.bow)
        return bow


class corpusDoc:
    '''
    The corpusDoc class is used to represent a single document within a corpus
    The docs propety of the inputCorpus class and the docs propety of the jamesCorpus
    class are both lists of these

    Attributes
    ----------

            title:
                    the title of the document as a string

            text:
                    the text of the document as a string

            lemmatized:
                    the text of the document in lemmatized form, as a list of strings

            bow:
                    the text of the document in bag of words form, as a list of (integer, integer) pairs

            sentences:
                    the text of the document separated into a list of sentences, where
                    each sentence is a string

    Methods
    -------
            addLemmatized(lemmatized):
                    This method is used to add the text of the document in lemmatized form
                    after preprocesing

            addBoW(bow):
                    This method is used to add the text of the document in bag of words form
                    after preprocessing

            addSentences(sentences):
                    This method is used to add a list of sentences in the document

    '''

    def __init__(self, title: str, text: str):
        '''
        corpusDoc is initialized with just the title and text of the document
        The other 3 attributes are initialized to empty lists

        Parameters
        ----------
                title:
                        the title of the document as a string

                text:
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
                lemmatized:
                        the text of the document in lemmatized form as a list of strings

        '''
        self.lemmatized = lemmatized

    def addBoW(self, bow):
        '''
        Parameters
        ----------
                bow:
                        the text of the document in bag of words form, as a list of
                        (integer, integer) pairs

        '''
        self.bow = bow

    def addSentences(self, sentences):
        '''
        Parameters
        ----------
                sentences:
                        the text of the document separated into a list of sentences, where
                        each sentence is a string

        '''
        self.sentences = sentences
