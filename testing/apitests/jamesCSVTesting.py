# Library imports
import json
import os
import sys
import unittest
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# Import the file to be tested
from api import jamesCSV
# Other required project imports
from api import jamesClasses, jamesMain
from api.jamesConfig import cfg

# Method for loading and constructing a test corpus from a file in testdata
def loadTestResponse():
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)),'testdata','testresponse.txt')
    f = open(filename,'r')
    testData = f.read()
    f.close()
    testResposne = json.loads(testData)
    return testResposne

# Load the test corpus into a constant
TESTRESPONSE = loadTestResponse()

# Tests for makeCSV method in jamesCSV
class TestJamesCSV_makeCSV(unittest.TestCase):
    # Test that makeCSV completes when no topics are hidden
    def test_make_no_hidden(self):
        output = jamesCSV.makeCSV(TESTRESPONSE)
        self.assertIsInstance(output,str)
    # Test that makeCSV completes when topics are hidden
    def test_make_hidden(self):
        output = jamesCSV.makeCSV(TESTRESPONSE,[1])
        self.assertIsInstance(output,str)

# Tests for createCSVList method in jamesCSV
class TestJamesCSV_createCSVList(unittest.TestCase):
    # Test that createCSVList completes when no topics are hidden
    def test_create_no_hidden(self):
        output = jamesCSV.createCSVList(TESTRESPONSE)
        self.assertIsInstance(output,list)
    # Test that createCSVList produces the correct structure
    #   when no topics are hidden
    def test_create_no_hidden_structure(self):
        output = jamesCSV.createCSVList(TESTRESPONSE)
        self.assertEqual(len(output),68)
        self.assertEqual(output[0],['Topics'])
        self.assertEqual(output[1][0],'Topic Model Coherence')
        self.assertIsInstance(output[1][1],float)
        self.assertEqual(output[2],['\n'])
        self.assertEqual(output[3],['Topic Number',1])
        self.assertEqual(output[4][0],'Topic Coherence')
        self.assertIsInstance(output[4][1],str)
        self.assertIsInstance(float(output[4][1]),float)
        self.assertEqual(output[5],['word','stem','weight'])
        for i in range(6,26):
            self.assertIsInstance(output[i][0],str)
            self.assertIsInstance(output[i][1],str)
            self.assertIsInstance(output[i][2],str)
            self.assertIsInstance(float(output[i][2]),float)
        self.assertEqual(output[26],['sentence','weight'])
        for i in range(27,32):
            self.assertIsInstance(output[i][0],str)
            self.assertIsInstance(output[i][1],str)
            self.assertIsInstance(float(output[i][1]),float)
        self.assertEqual(output[32],['\n'])
        self.assertEqual(output[33],['Topic Number',2])
        self.assertEqual(output[34][0],'Topic Coherence')
        self.assertIsInstance(output[34][1],str)
        self.assertIsInstance(float(output[34][1]),float)
        self.assertEqual(output[35],['word','stem','weight'])
        for i in range(36,56):
            self.assertIsInstance(output[i][0],str)
            self.assertIsInstance(output[i][1],str)
            self.assertIsInstance(output[i][2],str)
            self.assertIsInstance(float(output[i][2]),float)
        self.assertEqual(output[56],['sentence','weight'])
        for i in range(57,62):
            self.assertIsInstance(output[i][0],str)
            self.assertIsInstance(output[i][1],str)
            self.assertIsInstance(float(output[i][1]),float)
        self.assertEqual(output[62],['\n'])
        self.assertEqual(output[63],['Sentiment'])
        self.assertEqual(output[64][0],'Document Title')
        self.assertIsInstance(output[64][1],str)
        self.assertEqual(output[65],['topicnum','weight','sentiment'])
        for i in range(66,68):
            self.assertIsInstance(output[i][0],int)
            self.assertIsInstance(output[i][1],str)
            self.assertIsInstance(float(output[i][1]),float)
            self.assertIsInstance(output[i][2],str)
            self.assertIsInstance(float(output[i][2]),float)
    # Test that createCSVList completes when topics are hidden
    def test_create_hidden(self):
        output = jamesCSV.createCSVList(TESTRESPONSE,[1])
        self.assertIsInstance(output,list)
        # Test that createCSVList produces the correct structure
    #   when a topic is hidden
    def test_create_hidden_structure(self):
        output = jamesCSV.createCSVList(TESTRESPONSE,[1])
        self.assertEqual(len(output),37)
        self.assertEqual(output[0],['Topics'])
        self.assertEqual(output[1][0],'Topic Model Coherence')
        self.assertIsInstance(output[1][1],float)
        self.assertEqual(output[2],['\n'])
        self.assertEqual(output[3],['Topic Number',2])
        self.assertEqual(output[4][0],'Topic Coherence')
        self.assertIsInstance(output[4][1],str)
        self.assertIsInstance(float(output[4][1]),float)
        self.assertEqual(output[5],['word','stem','weight'])
        for i in range(6,26):
            self.assertIsInstance(output[i][0],str)
            self.assertIsInstance(output[i][1],str)
            self.assertIsInstance(output[i][2],str)
            self.assertIsInstance(float(output[i][2]),float)
        self.assertEqual(output[26],['sentence','weight'])
        for i in range(27,32):
            self.assertIsInstance(output[i][0],str)
            self.assertIsInstance(output[i][1],str)
            self.assertIsInstance(float(output[i][1]),float)
        self.assertEqual(output[32],['\n'])
        self.assertEqual(output[33],['Sentiment'])
        self.assertEqual(output[34][0],'Document Title')
        self.assertIsInstance(output[34][1],str)
        self.assertEqual(output[35],['topicnum','weight','sentiment'])
        self.assertIsInstance(output[36][0],int)
        self.assertIsInstance(output[36][1],str)
        self.assertIsInstance(float(output[36][1]),float)
        self.assertIsInstance(output[36][2],str)
        self.assertIsInstance(float(output[36][2]),float)

# Run the tests
if __name__ == '__main__':
    unittest.main()