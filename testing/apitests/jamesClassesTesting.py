

# Library imports
import os
import sys
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from api.jamesClasses import *

import unittest

class TestjamesClasses1(unittest.TestCase):

    def setUp(self):

        self.file1 = os.path.join(os.path.dirname(os.path.dirname(__file__)),'testdata','testdata1.txt')
        self.file2 = os.path.join(os.path.dirname(os.path.dirname(__file__)),'testdata','testdata2.txt')
        f1 = open(self.file1, "r")
        self.text1 = f1.read()
        f1.close()
        f2 = open(self.file2, "r")
        self.text2 = f2.read()
        f2.close()

    # testing of the classes inputCorpus, corpusDoc, and jamesCorpus
    def test_inputCorpus_corpusDoc_jamesCorpus(self):
        # inputCorpus initialization
        self.inputCorpus = inputCorpus()
        # the docs variable is initialized to an empty list
        self.assertEqual(self.inputCorpus.docs, [])
        # and is length 0
        self.assertEqual(len(self.inputCorpus.docs), 0)
        # the addDoc() method has two parameters, a title, and text
        # these parameters are type-checked via the assert statement combined with isinstance()
        # which is appended to the list as a corpusDoc object
        # assertRaises will return false if the assertionError is not called
        self.assertRaises(AssertionError, self.inputCorpus.addDoc, 1,2)
        self.assertRaises(AssertionError, self.inputCorpus.addDoc, 1, "str")
        self.assertRaises(AssertionError, self.inputCorpus.addDoc, "str", 1)
        self.assertRaises(AssertionError, self.inputCorpus.addDoc, 5.09,-0.56)
        self.assertRaises(AssertionError, self.inputCorpus.addDoc, "str", ["str"])
        self.assertRaises(AssertionError, self.inputCorpus.addDoc, True, False)
        self.inputCorpus.addDoc(self.file1, self.text1)
        # is now length 1
        self.assertEqual(len(self.inputCorpus.docs), 1)
        # list index 0 is a corpusDoc with variables title and text, file1 and text1
        self.assertEqual(self.inputCorpus.docs[0].title, self.file1)
        self.assertEqual(self.inputCorpus.docs[0].text, self.text1)
        # add another document title and text
        self.inputCorpus.addDoc(self.file2, self.text2)
        # is now length 2
        self.assertEqual(len(self.inputCorpus.docs), 2)
        # list index 1 is a corpusDoc with variables title and text, file2 and text2
        self.assertEqual(self.inputCorpus.docs[1].title, self.file2)
        self.assertEqual(self.inputCorpus.docs[1].text, self.text2)

        # corpusDoc
        # the corpusDoc() method has two parameters, a title, and text
        # these parameters are type-checked via the assert statement combined with isinstance()
        # assertRaises will return false if the assertionError is not called
        self.assertRaises(AssertionError, corpusDoc, 1, 2)
        self.assertRaises(AssertionError, corpusDoc, 1, "str")
        self.assertRaises(AssertionError, corpusDoc, "str", 1)
        self.assertRaises(AssertionError, corpusDoc, 5.09, -0.56)
        self.assertRaises(AssertionError, corpusDoc, "str", ["str"])
        self.assertRaises(AssertionError, corpusDoc, True, False)
        # initialize two corpusDoc objects with the titles and texts
        self.corpusDoc1 = corpusDoc(self.file1, self.text1)
        self.corpusDoc2 = corpusDoc(self.file2, self.text2)
        # corpusDoc1 title and text variables are file1 and text1
        self.assertEqual(self.corpusDoc1.title, self.file1)
        self.assertEqual(self.corpusDoc1.text, self.text1)
        # corpusDoc1 lemmatized variable is initialized an empty list
        self.assertEqual(self.corpusDoc1.lemmatized, [])
        # the addLemmetized Method allows only a list for its parameter
        self.assertRaises(AssertionError, self.corpusDoc1.addLemmatized, True)
        self.assertRaises(AssertionError, self.corpusDoc1.addLemmatized, 0.5)
        self.assertRaises(AssertionError, self.corpusDoc1.addLemmatized, -12)
        self.assertRaises(AssertionError, self.corpusDoc1.addLemmatized, {})
        self.assertRaises(AssertionError, self.corpusDoc1.addLemmatized, "str")
        # storing a list of integers
        self.numbers = [1, 2, 3, 4, 5]
        # add a list to the lemmatized field
        self.corpusDoc1.addLemmatized(self.numbers)
        # corpusDoc1 lemmatized variable is a list of 5 numbers
        self.assertEqual(self.corpusDoc1.lemmatized, self.numbers)
        # corpusDoc1 bow variable is initialized an empty list
        self.assertEqual(self.corpusDoc1.bow, [])
        # the addBoW Method allows only a list for its parameter
        self.assertRaises(AssertionError, self.corpusDoc1.addBoW, True)
        self.assertRaises(AssertionError, self.corpusDoc1.addBoW, 0.5)
        self.assertRaises(AssertionError, self.corpusDoc1.addBoW, -12)
        self.assertRaises(AssertionError, self.corpusDoc1.addBoW, {})
        self.assertRaises(AssertionError, self.corpusDoc1.addBoW, "str")
        # add a list to the bow field
        self.corpusDoc1.addBoW(self.numbers)
        # corpusDoc1 bow variable is an list of 5 numbers
        self.assertEqual(self.corpusDoc1.bow, self.numbers)
        # corpusDoc1 sentences variable is initialized an empty list
        self.assertEqual(self.corpusDoc1.sentences, [])
        # the addSentences Method allows only a list for its parameter
        self.assertRaises(AssertionError, self.corpusDoc1.addSentences, True)
        self.assertRaises(AssertionError, self.corpusDoc1.addSentences, 0.5)
        self.assertRaises(AssertionError, self.corpusDoc1.addSentences, -12)
        self.assertRaises(AssertionError, self.corpusDoc1.addSentences, {})
        self.assertRaises(AssertionError, self.corpusDoc1.addSentences, "str")
        # add a list to the sentences field
        self.corpusDoc1.addSentences(self.numbers)
        # corpusDoc1 sentences variable is a list of 5 numbers
        self.assertEqual(self.corpusDoc1.sentences, self.numbers)

        # jamesCorpus
        # jamesCorpus parameters are a list, a dictionary, and a dictionary
        self.assertRaises(AssertionError, jamesCorpus, "str", {}, {})
        self.assertRaises(AssertionError, jamesCorpus, [], {}, 1)
        self.assertRaises(AssertionError, jamesCorpus,  -12,  0.0005, {})
        self.assertRaises(AssertionError, jamesCorpus, [], [], [])
        self.assertRaises(AssertionError, jamesCorpus, {}, {}, {})
        # initialize jamesCorpus1 with parameters empty list, empty dict, empty dict
        self.jamesCorpus1 = jamesCorpus([], {}, {})
        # jamesCorpus1 variables docs, dic, and stemDic are empty lists
        # the methods getBoW() and getLemmatized() return empty lists because the docs variable is empty list
        self.assertEqual(self.jamesCorpus1.docs, [])
        self.assertEqual(self.jamesCorpus1.dic, {})
        self.assertEqual(self.jamesCorpus1.stemDic, {})
        self.assertEqual(self.jamesCorpus1.getBoW(), [])
        self.assertEqual(self.jamesCorpus1.getLemmatized(), [])
        # store a list of the corpusDoc objects
        self.listOfcorpusDocs = [self.corpusDoc1, self.corpusDoc2]
        # initialize jamesCorpus2 with the list above, and a dictionary
        self.dictionary = {'x': 1, 'y':2}
        self.jamesCorpus2 = jamesCorpus(self.listOfcorpusDocs, self.dictionary, self.dictionary)
        # jamesCorpus2 docs variable was initialized with corpusDocs
        self.assertEqual(self.jamesCorpus2.docs, self.listOfcorpusDocs)
        # the docs variable has two corpusDocs objects. The titles and texts for both are correct
        self.assertEqual(self.jamesCorpus2.docs[0].title, self.corpusDoc1.title)
        self.assertEqual(self.jamesCorpus2.docs[0].text, self.corpusDoc1.text)    # corpusDoc1 and corpusDoc2
        self.assertEqual(self.jamesCorpus2.docs[1].title, self.corpusDoc2.title)
        self.assertEqual(self.jamesCorpus2.docs[1].text, self.corpusDoc2.text)
        # corpusDoc1 has an entry for lemmas and BoW's but corpusDoc2 did not
        self.assertEqual(self.jamesCorpus2.getLemmatized(), [self.numbers, []])
        self.assertEqual(self.jamesCorpus2.getBoW(), [self.numbers, []])
        # we can add entries to these variables with the methods for each
        self.corpusDoc2.addLemmatized(self.numbers)
        self.corpusDoc2.addBoW(self.numbers)
        # jamesCorpus2 lemma's and BoW's are correctly adjusted
        self.assertEqual(self.jamesCorpus2.getLemmatized(), [self.numbers, self.numbers])
        self.assertEqual(self.jamesCorpus2.getBoW(), [self.numbers, self.numbers])

class TestjamesClasses2(unittest.TestCase):

    # unit tests for classes docTopic and docResults
    def test_docTopic_docResults(self):

        # docTopic
        # docTopic objects initialize with a tuple of integer and float parameters
        self.assertRaises(AssertionError, docTopic, {})
        self.assertRaises(AssertionError, docTopic, 1)
        self.assertRaises(AssertionError, docTopic, "str")
        self.assertRaises(AssertionError, docTopic, False)
        # first parameter of tuple must be type int and non-negative
        # second parameter of tuple must be type float and non-negative
        self.assertRaises(AssertionError, docTopic, ("str", 1.5))
        self.assertRaises(AssertionError, docTopic, (1, "str"))
        self.assertRaises(AssertionError, docTopic, (-1, 1.6))
        self.assertRaises(AssertionError, docTopic, (10, -0.06))
        self.assertRaises(AssertionError, docTopic, (1.567, 1.67))
        self.assertRaises(AssertionError, docTopic, (45, -1))
        self.assertRaises(AssertionError, docTopic, ([], 0.09))
        self.assertRaises(AssertionError, docTopic, (9, {}))
        # create docTopic object with tuple (int, float)
        self.docTopic1 = docTopic((0, 0.3))
        # the topicNum variable is the first input parameter + 1 (was 0)
        self.assertEqual(self.docTopic1.topicNum, 1)
        # the weight variable is the second input paramater (was 0.3)
        self.assertEqual(self.docTopic1.weight, 0.3)
        # sentimentTotal variable is initialized 0.0
        self.assertEqual(self.docTopic1.sentimentTotal, 0.0)
        # the sentimentWeight variable is initialized 0.0
        self.assertEqual(self.docTopic1.sentimentWeight, 0.0)
        # the expected output for initial call to output()
        # the topicNum, weight, and sentimentTotal variables in a dictionary
        self.docTopic1Output1 = {"topicnum": 1, "weight": str(0.3), "sentiment": str(0.0)}
        self.assertEqual(self.docTopic1.output(), self.docTopic1Output1)
        # call to addSentiment takes parameters weight and a sentiment of types float
        # the weight parameter (first) must be non-negative
        self.assertRaises(AssertionError, self.docTopic1.addSentiment, -1, 0.5)
        self.assertRaises(AssertionError, self.docTopic1.addSentiment, "str", 0.5)
        self.assertRaises(AssertionError, self.docTopic1.addSentiment, 0.5, "str")
        self.docTopic1.addSentiment(0.5,0.5)
        # the expected value of sentimentTotal variable
        self.newSentimentTotal1 = 0.5 * 0.5
        self.assertEqual(self.docTopic1.sentimentTotal, self.newSentimentTotal1)
        # the expected value of sentimentWeight variable
        self.newSentimentWeight1 = 0.5
        self.assertEqual(self.docTopic1.sentimentWeight, self.newSentimentWeight1)
        # call to averageSentiments() will perform division of sentimentTotal by sentimentWeight
        self.docTopic1.averageSentiments()
        # the expected value for sentimentTotal variable
        self.newSentimentTotal2 = self.newSentimentTotal1 / self.newSentimentWeight1
        self.assertEqual(self.docTopic1.sentimentTotal, self.newSentimentTotal2)
        # the expected output of the new call to output()
        self.docTopic1Output2 = {"topicnum": 1, "weight": str(0.3), "sentiment": str(self.newSentimentTotal2)}
        self.assertEqual(self.docTopic1.output(), self.docTopic1Output2)

        # docResults
        # docResults objects are initialized with title, type 'str', and topics, type 'list' of tuple (int, float)
        self.assertRaises(AssertionError, docResults, 'str', 0.5)
        self.assertRaises(AssertionError, docResults, 'str', 'str')
        self.assertRaises(AssertionError, docResults, 1, [(5, 0.5)])
        self.assertRaises(AssertionError, docResults, {}, [(5, 0.5)])
        self.assertRaises(AssertionError, docResults, 1.9, [(5, 0.5)])
        self.assertRaises(AssertionError, docResults, [0,9], [(5, 0.5)])
        self.assertRaises(AssertionError, docResults,  'str', [(7, 0.5), ( 'str', 0.97)])
        self.assertRaises(AssertionError, docResults, 'str', [(7, 0.5), (91, {})])
        self.assertRaises(AssertionError, docResults, 'str', [(7, 0.5), (-1, 0.56)])
        # store a second docTopic object
        self.docTopic2 = docTopic((1, 0.7))
        # the first parameter to docResults object
        self.title = "title"
        # the second parameter to docResults object,
        # the values will be store in docTopic objects, same as docTopic1 and docTopic2
        self.topics = [(0, 0.3), (1, 0.7)]
        # initialize docResults object
        self.docResults1 = docResults(self.title, self.topics)
        # the expect results for docTopic2 call to output() is stored
        self.docTopic2Output1 = {"topicnum": 2, "weight": str(0.7), "sentiment": str(0.0)}
        # the four parameters are used to alter the sentimentTotal variable of a docTopic with addSentiment() method
        self.weights1 = 0.2
        self.weights2 = 0.3
        self.sentiments1 = 0.4
        self.sentiments2 = 0.5
        # initialized docResult object first parameter is the title  # can be any type
        self.assertEqual(self.docResults1.docTitle, self.title)
        # initialized docResult object second parameter, first tuple, first index is the docTopic1 topicNum variable
        self.assertEqual(self.docResults1.docTopics[0].topicNum, self.docTopic1.topicNum)
        # the second parameter, first tuple, second index is the docTopic1 weight variable
        self.assertEqual(self.docResults1.docTopics[0].weight, self.docTopic1.weight)
        # the second parameter, second tuple, first index is the docTopic2 topicNum variable
        self.assertEqual(self.docResults1.docTopics[1].topicNum, self.docTopic2.topicNum)
        # the second parameter, second tuple, second index is the docTopic2 weight variable
        self.assertEqual(self.docResults1.docTopics[1].weight, self.docTopic2.weight)
        # store a list of docTopic object outputs()
        self.topicsOutput1 = [self.docTopic1Output1, self.docTopic2Output1]
        # the expected output of docResults first call to output(), is title and above list in a dictionary
        self.docResults1Output1 = {"doctitle": self.title, "topics": self.topicsOutput1}
        self.assertEqual(self.docResults1.output(), self.docResults1Output1)
        # the addSentiment() method takes a topic number type int, weight type float, and sentiment type float
        # the integer parameter must be in the range of '0' : total number of topics, currently '2'
        self.assertRaises(AssertionError, self.docResults1.addSentiment, 3, self.weights1, self.sentiments1)
        self.assertRaises(AssertionError, self.docResults1.addSentiment, -1, self.weights1, self.sentiments1)
        self.assertRaises(AssertionError, self.docResults1.addSentiment, 1, self.weights1, {})
        self.assertRaises(AssertionError, self.docResults1.addSentiment, 1, -self.weights1, self.sentiments1)
        self.assertRaises(AssertionError, self.docResults1.addSentiment, 2, self.weights1, [1])
        # the call to addSentiment() for topic 1 will change docTopic[0]
        self.docResults1.addSentiment(1, self.weights1, self.sentiments1)
        # the expected change to sentimentTotal parameter of docTopic[0]
        self.docResultsSentimentTotal1 = self.sentiments1 * self.weights1
        self.assertEqual(self.docResults1.docTopics[0].sentimentTotal, self.docResultsSentimentTotal1)
        # the expected change to sentimentWeight parameter of docTopic[0]
        self.assertEqual(self.docResults1.docTopics[0].sentimentWeight, self.weights1)
        # the second call to addsentiment() for topic 1 will again change docTopic[0]
        self.docResults1.addSentiment(1, self.weights2, self.sentiments2)
        # the expected change to sentimentTotal parameter of docTopic[0]
        self.docResultsSentimentTotal2 = self.docResultsSentimentTotal1 + self.sentiments2 * self.weights2
        self.assertEqual(self.docResults1.docTopics[0].sentimentTotal, self.docResultsSentimentTotal2)
        # the expected output for docTopic[0] call to output()
        self.docTopic1Output2 = {"topicnum": 1, "weight": str(0.3), "sentiment": str(self.docResultsSentimentTotal2)}
        # the expected output docTopic[1] call to output() (no change)
        self.docTopic2Output2 = {"topicnum": 2, "weight": str(0.7), "sentiment": str(0.0)}
        # store a new list of docTopic object outputs()
        self.topicsOutput2 = [self.docTopic1Output2, self.docTopic2Output2]
        # the expected output of docResults second call to output(), is title and above list in a dictionary
        self.docResults1Output2 = {"doctitle": self.title, "topics": self.topicsOutput2}
        self.assertEqual(self.docResults1.output(), self.docResults1Output2)
        # the method averageSentiments() will alter the sentimentTotal variable of all n docTopics up to docTopic[n-1].
        self.docResults1.averageSentiments()
        # the expected change to sentimentTotal after above method call
        self.docResultsSentimentTotal3 = self.docResultsSentimentTotal2 / (self.weights1 + self.weights2)
        # the expected output of all docTopics[0] and docTopics[1] call to output()
        self.docTopic1Output3 = {"topicnum": 1, "weight": str(0.3), "sentiment": str(self.docResultsSentimentTotal3)}
        self.docTopic2Output3 = {"topicnum": 2, "weight": str(0.7), "sentiment": str(0.0)}
        # the the new list of docTopic object outputs()
        self.topicsOutput3 = [self.docTopic1Output3, self.docTopic2Output3]
        # the expected output of docResults third call to output() is title and above list in a dictionary
        self.docResults1Output3 = {"doctitle": self.title, "topics": self.topicsOutput3}
        self.assertEqual(self.docResults1.output(), self.docResults1Output3)

class TestjamesClasses3(unittest.TestCase):

    # unit tests for classes topicWord, topicReulsts, and jamesResults
    def test_topicWord_topicResults_jamesResults(self):

        # topicWord
        # topicWord objects initialize with a tuple parameter of type (float, str)
        self.assertRaises(AssertionError, topicWord, {})
        self.assertRaises(AssertionError, topicWord, "str")
        self.assertRaises(AssertionError, topicWord, 1)
        self.assertRaises(AssertionError, topicWord, (6.9, []))
        self.assertRaises(AssertionError, topicWord, ([], "str"))
        # store tuples
        self.tuple1 = (0.59, "stem1")
        self.tuple2 = (0.75, "stem2")
        # create topicWord objects with a tuple parameter
        self.topicWord1 = topicWord(self.tuple1)
        self.topicWord2 = topicWord(self.tuple2)
        # store a dictionary for the strings of the tuples
        self.dict1 = {"stem1": "word1", "stem2": "word2"}
        self.dict2 = {"missingStem1": "wordMissing1", "stem2": "word2"}
        # the topicWord.output() method takes a parameter of type 'dict'
        self.assertRaises(AssertionError, self.topicWord1.output, 1)
        self.assertRaises(AssertionError, self.topicWord1.output, [])
        self.assertRaises(AssertionError, self.topicWord1.output, "str")
        # the dictionary input parameter must have an entry for the stem word of a topicWord object
        self.assertRaises(AssertionError, self.topicWord1.output, self.dict2)
        # the method returns a dictionary as output
        self.topicWord1output1 = {"word": self.dict1[self.topicWord1.word], "weight": str(self.topicWord1.weight)}
        self.assertEqual(self.topicWord1.output(self.dict1), self.topicWord1output1)


        # topicResults
        # topicResult objects initialize with a topic number, type int, and a result, of type tuple
        # result tuple must be of type (list, float), inner list must be of type tuple of form (float, string)
        self.assertRaises(AssertionError, topicResults, 1, ())
        self.assertRaises(AssertionError, topicResults, 1, [])
        self.assertRaises(AssertionError, topicResults, 1, "str")
        self.assertRaises(AssertionError, topicResults, 1, ([], 5.6))
        self.assertRaises(AssertionError, topicResults, 1, ([(1.5, 1.5)], 5.6))
        self.assertRaises(AssertionError, topicResults, 1, ([("str", "str")], 5.6))
        self.assertRaises(AssertionError, topicResults, 1, ([(1.5, "str")], {}))
        self.assertRaises(AssertionError, topicResults, 1, ([(1.5, "str")], []))
        self.assertRaises(AssertionError, topicResults, 1, ([(1.5, "str")], "str"))
        # store a topic number, coherence score and results object
        self.topicNum = 1
        self.coherenceScore1 = 0.678
        self.results1 = ([self.tuple1, self.tuple2], self.coherenceScore1)
        # create the topicResults object with above parameters
        self.topicResults1 = topicResults(self.topicNum, self.results1)
        # the topicResult1.output method takes a dictionary parameter and returns a dictionary
        # with keys "topicnum", "coherence", and topicwords.
        self.wordsOut = [self.topicWord1.output(self.dict1), self.topicWord2.output(self.dict1)]
        self.topicResults1output1 = {"topicnum": self.topicNum, "coherence": str(self.coherenceScore1),
                                     "topicwords": self.wordsOut}
        # find the output of topicResults1
        self.assertEqual(self.topicResults1.output(self.dict1), self.topicResults1output1)
        # the dictionary input parameter must have an entry for all stem words
        # of a topicResults object to produce output method results
        self.assertRaises(AssertionError, self.topicResults1.output, self.dict2)

        # jamesResults
        # jamesResults objects are initialized with parameter type: list of (list of (float, str), float)
        # which defines the results of the top topics of an LDA model,
        # including words, word weights, and coherence scores to define the topics
        self.assertRaises(AssertionError, jamesResults, {})
        self.assertRaises(AssertionError, jamesResults, -5)
        self.assertRaises(AssertionError, jamesResults, "str")
        self.assertRaises(AssertionError, jamesResults, [])
        self.assertRaises(AssertionError, jamesResults, [([("str", 0.5)], 5.5)])
        self.assertRaises(AssertionError, jamesResults, [([(0.5, 0.5)], 5.5)])
        self.assertRaises(AssertionError, jamesResults, [([(0.5, "str")], "str")])
        self.assertRaises(AssertionError, jamesResults, [([(0.5, "str")], [])])
        # store float, string, and list, values to build input to jamesResults object
        self.float1 = 5.5
        self.float2 = 0.987
        self.string1 = "stem1"
        self.string2 = "stem2"
        self.list1 = [(self.float1, self.string1), (self.float1, self.string2)]
        self.list2 = [(self.list1, self.float2)]
        # build object
        self.jamesResults1 = jamesResults(self.list2)
        # the addDocResults method stores a docResults object to an internal variable of jamesResults objects
        self.assertRaises(AssertionError, self.jamesResults1.addDocResults, {})
        self.assertRaises(AssertionError, self.jamesResults1.addDocResults, "str")
        self.assertRaises(AssertionError, self.jamesResults1.addDocResults, 1)
        self.assertRaises(AssertionError, self.jamesResults1.addDocResults, -0.06)
        # initialize docResults object
        self.title = "title"
        self.topics = [(0, 0.3), (1, 0.7)]
        self.docResults1 = docResults(self.title, self.topics)
        # add the docResults
        self.jamesResults1.addDocResults(self.docResults1)
        # the docResults are appended to internal list
        self.assertEqual(self.jamesResults1.documentResults, [self.docResults1])
        # the addStemDic method stores a dictionary mapping stems to words (lemmas)
        self.assertRaises(AssertionError, self.jamesResults1.addStemDic, [])
        self.assertRaises(AssertionError, self.jamesResults1.addStemDic, "str")
        self.assertRaises(AssertionError, self.jamesResults1.addStemDic, 1)
        self.assertRaises(AssertionError, self.jamesResults1.addStemDic, -0.06)
        # call the method
        self.jamesResults1.addStemDic(self.dict1)
        # the dictionary is stored with internal variable to jamesResults object
        self.assertEqual(self.jamesResults1.stemDic, self.dict1)
        # the getNumberofTopics method returns the total topics in the results
        # the jamesResult1 object was intiallized with self.list2, length 1.
        self.assertEqual(self.jamesResults1.getNumberOfTopics(), len(self.list2))
        self.assertEqual(self.jamesResults1.getNumberOfTopics(), 1)
        # the jamesResults output method returns a dictionary of results
        # the jamesResults1 object was initialized with a one topic LDA result (self.list2)
        # that one topic is stored in a topicResults object as topic 1
        # so we store our expected results
        self.topicResults2 = topicResults(1, self.list2[0])
        # we also added a docResults to the jamesResult1 object with parameters (self.docResults1)
        # each value in the dictionary of results is a list, one for topic results, one for document results
        # we store them
        self.topicsOut = [self.topicResults2.output(self.dict1)]
        self.documentsOut = [self.docResults1.output()]
        # we store the expected result of the output() method
        self.jamesResults1output1 = {"topics": self.topicsOut, "sentiments": self.documentsOut}
        # lastly we check
        self.assertEqual(self.jamesResults1.output(), self.jamesResults1output1)


if __name__ == '__main__':
    unittest.main()