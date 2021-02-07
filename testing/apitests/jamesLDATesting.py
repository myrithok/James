# Library imports
import gensim
import os
import sys
import unittest
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# Import the file to be tested
from api import jamesLDA
# Other required project imports
from api import jamesClasses, jamesPreProcessing
from api.jamesConfig import cfg

# Method for loading and constructing a test corpus from a file in testdata
def loadTestCorpus():
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'testdata','testdata.txt')
    f = open(filename,'r')
    testData = f.read()
    f.close()
    inputCorpus = jamesClasses.inputCorpus()
    inputCorpus.addDoc("test",testData)
    testCorpus = jamesPreProcessing.preProcess(inputCorpus)
    return testCorpus

# Method for loading and constructing a test LDA model from files in testdata
def loadTestModel():
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'testdata','testmodel')
    testModel = gensim.models.ldamodel.LdaModel.load(filename)
    return testModel

# Method for loading and constructing a test sentence from the test corpus and
#    a file in testdata
def loadTestSentence(testCorpus,number=""):
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'testdata','testsentence' + number + '.txt')
    f = open(filename,'r')
    rawSentence= f.read()
    f.close()
    testSentence = jamesPreProcessing.preProcessSentence(rawSentence, testCorpus.dic)
    return testSentence

# Load the test corpus, test model, and test sentence into constants
TESTCORPUS = loadTestCorpus()
TESTMODEL = loadTestModel()
TESTSENTENCEONE = loadTestSentence(TESTCORPUS,"one")
TESTSENTENCETWO = loadTestSentence(TESTCORPUS,"two")

# Tests for buildTopicModel method in jamesLDA
class TestJamesLDA_buildTopicModel(unittest.TestCase):
    # Test that the correct output type is produced when the number of
    #    topics is specified
    def test_specified_topicnum(self):
        for i in range(1,4):
            testmodel = jamesLDA.buildTopicModel(TESTCORPUS,i)
            self.assertIsInstance(testmodel,gensim.models.ldamodel.LdaModel)
    # Test that the correct number of topics are constructed when the
    #    number of topics is specified
    def test_specified_topicnum_has_correct_topic_num(self):
        for i in range(1,4):
            testmodel = jamesLDA.buildTopicModel(TESTCORPUS,i)
            self.assertEqual(len(testmodel.get_topics()), i)
    # Test that the correct output type is produced when the number of
    #    topics is not specified
    def test_unspecified_topicnum(self):
        testmodel = jamesLDA.buildTopicModel(TESTCORPUS,None)
        self.assertIsInstance(testmodel,gensim.models.ldamodel.LdaModel)
    # Test that the generated topic model identifies important words
    def test_topic_generation(self):
        testmodel = jamesLDA.buildTopicModel(TESTCORPUS,2)
        testtopics = testmodel.top_topics(TESTCORPUS.getBoW(),topn=5)
        topicwords = []
        for topic in testtopics:
            for word in topic[0]:
                topicwords.append(word[1])
        self.assertTrue('netflix' in topicwords or 'netflix' in topicwords)
        self.assertTrue('chip' in topicwords or 'chip' in topicwords)
        
# Tests for the buildBestCoherenceTopicModel method in jamesLDA
class TestJamesLDA_buildBestCoherenceTopicModel(unittest.TestCase):
    # Test that the correct output type is produced
    def test_builds_mallet_model(self):
        testmodel = jamesLDA.buildBestCoherenceTopicModel(TESTCORPUS)
        self.assertIsInstance(testmodel,gensim.models.wrappers.ldamallet.LdaMallet)
    # Test that the model chosen actually has the highest coherence score
    def test_best_coherence_is_chosen(self):
        testmodel = jamesLDA.buildBestCoherenceTopicModel(TESTCORPUS)
        testcoherence = gensim.models.coherencemodel.CoherenceModel(model=testmodel,texts=TESTCORPUS.getLemmatized(),dictionary=TESTCORPUS.dic,corpus=TESTCORPUS.getBoW(),coherence="c_v")
        testscore = testcoherence.get_coherence()
        for i in range(2, cfg['topicmax'] + 1):
            tempmodel = jamesLDA.buildMalletModel(TESTCORPUS, i)
            tempcoherence = gensim.models.coherencemodel.CoherenceModel(model=tempmodel,texts=TESTCORPUS.getLemmatized(),dictionary=TESTCORPUS.dic, corpus=TESTCORPUS.getBoW(),coherence="c_v")
            tempscore = tempcoherence.get_coherence()
            self.assertLessEqual(tempscore,testscore)

# Tests for the buildMalletModel method in jamesLDA
class TestJamesLDA_buildMalletModel(unittest.TestCase):
    # Test that the correct output type is produced
    def test_topics(self):
        for i in range(1,4):
            testmodel = jamesLDA.buildMalletModel(TESTCORPUS,i)
            self.assertIsInstance(testmodel,gensim.models.wrappers.ldamallet.LdaMallet)
    # Test that the correct number of topics are constructed
    def test_has_correct_topic_num(self):
        for i in range(1,4):
            testmodel = jamesLDA.buildMalletModel(TESTCORPUS,i)
            self.assertEqual(len(testmodel.get_topics()), i)

# Tests for the getResults method in jamesLDA
class TestJamesLDA_getResults(unittest.TestCase):
    # Test that the correct output type is produced
    def test_produces_results(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        self.assertIsInstance(testresults,jamesClasses.jamesResults)
    # Test that the stemDic property of the output results is an
    #    empty dictionary
    def test_results_stemDic_empty(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        self.assertEqual(testresults.stemDic,{})
    # Test that the documentResults property of the output results is
    #    an empty list
    def test_results_documentResults_empty(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        self.assertEqual(testresults.documentResults,[])
    # Test that the topicResults property of the output results is
    #    not an empty list
    def test_results_has_topics(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        self.assertIsNot(testresults.topicResults,[])
    # Test that the topics in the output results are the correct type
    def test_results_topics_are_topics(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        for topic in testresults.topicResults:
            self.assertIsInstance(topic,jamesClasses.topicResults)
    # Test that the topic list in the output results has the correct
    #     number of topics
    def test_results_correct_topic_count(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        self.assertEqual(len(testresults.topicResults),2)
    # Test that the topics in the output results are correctly numbered
    def test_results_correct_topic_numbers(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        topicnumbers = []
        for topic in testresults.topicResults:
            topicnumbers.append(topic.topicNum)
        topicnumbers.sort()
        self.assertEqual(topicnumbers,[1,2])
    # Test that the topics in the output results have topic words
    def test_results_topics_have_words(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        topicnumbers = []
        for topic in testresults.topicResults:
            self.assertIsNot(topic.topicWords,[])
    # Test that the words in each topic of the output results are
    #    the correct type
    def test_results_topic_words_are_words(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        topicnumbers = []
        for topic in testresults.topicResults:
            for word in topic.topicWords:
                self.assertIsInstance(word,jamesClasses.topicWord)
    # Test that the words in each topic of the output results have
    #    attributes of the correct types
    def test_results_topic_words_have_attributes(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        topicnumbers = []
        for topic in testresults.topicResults:
            for word in topic.topicWords:
                self.assertIsInstance(word.word,str)
                self.assertIsInstance(word.weight,float)
    # Test that each topic in the output results have the correct
    #    number of words
    def test_results_correct_word_count(self):
        testresults = jamesLDA.getResults(TESTMODEL,TESTCORPUS)
        for topic in testresults.topicResults:
            self.assertEqual(len(topic.topicWords),cfg['topicwords'])

# Tests for the getTopics method in jamesLDA
class TestJamesLDA_getTopics(unittest.TestCase):
    # Test that the correct output type is produced
    def test_produces_topics(self):
        testtopics = jamesLDA.getTopics(TESTSENTENCEONE,TESTMODEL)
        self.assertIsInstance(testtopics,list)
    # Test that the output contains the correct number of topics
    def test_correct_topic_number(self):
        testtopics = jamesLDA.getTopics(TESTSENTENCEONE,TESTMODEL)
        self.assertEqual(len(testtopics),2)
    # Test that the output probabilities sum to 1
    def test_probabilities_sum_to_one(self):
        testtopics = jamesLDA.getTopics(TESTSENTENCEONE,TESTMODEL)
        self.assertEqual(testtopics[0][1] + testtopics[1][1],1)
    # Test that sentence topics are correctly identified
    def test_topic_identification(self):
        testtopicsone = jamesLDA.getTopics(TESTSENTENCEONE,TESTMODEL)
        testtopicstwo = jamesLDA.getTopics(TESTSENTENCETWO,TESTMODEL)
        self.assertGreater(testtopicsone[0][1],testtopicstwo[0][1])
        self.assertLess(testtopicsone[1][1],testtopicstwo[1][1])

# Run tests
if __name__ == '__main__':
    unittest.main()