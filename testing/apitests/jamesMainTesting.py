# Library imports
import os
import sys
import unittest
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# Import the file to be tested
from api import jamesMain
# Other required project imports
from api import jamesClasses

# Method for loading and constructing a test corpus from a file in testdata
def loadTestCorpus():
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'testdata','testdata1.txt')
    f = open(filename,'r')
    testData = f.read()
    f.close()
    testCorpus = jamesClasses.inputCorpus()
    testCorpus.addDoc("test",testData)
    return testCorpus

# Load the test corpus into a constant
TESTCORPUS = loadTestCorpus()

# Tests for process method in jamesMain
class TestJamesMain_process(unittest.TestCase):
    # Test that a correct object type is output when the number of topics is specified
    def test_specified_topics(self):
        self.assertIsInstance(jamesMain.process(TESTCORPUS,1),dict)
    # Test that a correct object type is output when the number of topics is not specified
    def test_unspecified_topics(self):
        self.assertIsInstance(jamesMain.process(TESTCORPUS),dict)
    # Test that the output contains the expected structure
    def test_required_output(self):
        testoutput = jamesMain.process(TESTCORPUS,1)
        self.assertIsInstance(testoutput['topics'],list)
        for topic in testoutput['topics']:
            self.assertIsInstance(topic['topicnum'],int)
            self.assertIsInstance(topic['coherence'],str)
            self.assertIsInstance(topic['topicwords'],list)
            for word in topic['topicwords']:
                self.assertIsInstance(word['word'],str)
                self.assertIsInstance(word['weight'],str)
        self.assertIsInstance(testoutput['sentiments'],list)
        for sentiment in testoutput['sentiments']:
            self.assertIsInstance(sentiment['doctitle'],str)
            self.assertIsInstance(sentiment['topics'],list)
            for topic in sentiment['topics']:
                self.assertIsInstance(topic['topicnum'],int)
                self.assertIsInstance(topic['weight'],str)
                self.assertIsInstance(topic['sentiment'],str)

# Run the tests
if __name__ == '__main__':
    unittest.main()