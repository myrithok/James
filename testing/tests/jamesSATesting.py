# Library imports
import os
import sys
import unittest
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# Import the file to be tested
from api.jamesSA import buildSentimentModel, prepareTrainingData, getTokenDic, saveSentimentModel, loadSentimentModel, getSentenceSentiment
# Other required project imports
from api.jamesConfig import cfg


class TestSA(unittest.TestCase):
    def test_prepareTrainingData(self):
        data1 = cfg['satraining']
        self.assertEqual(isinstance(data1, dict), True)

        ret = prepareTrainingData(data1)
        self.assertEqual(isinstance(ret, list), True)

    def test_getTokenDic(self):
        tokenList = ["test", "case"]
        x = getTokenDic(tokenList)
        for token in x:
            self.assertEqual(isinstance(token, dict), True)

    def test_SentimentModel(self):
        # Load training data
        data = cfg['satraining']
        self.assertEqual(isinstance(data, dict), True)

        # train a classifier
        classifier = buildSentimentModel(cfg['satraining'])

        # save the classifier to file
        saveSentimentModel(os.path.join(os.path.dirname(__file__),'testdata','testSAModel.pickle'), cfg['satraining'])

        # test the sentiment scoring by making a prediction
        x1 = getSentenceSentiment("Very bad", classifier)
        self.assertEqual(x1 < 0, True)

        x2 = getSentenceSentiment("So good so happy", classifier)
        self.assertEqual(x2 > 0, True)

    def test_loadSentimentModel(self):
        # load a model
        model = loadSentimentModel(os.path.join(os.path.dirname(__file__),'testdata','testSAModel.pickle'))

        # test the sentiment scoring
        x1 = getSentenceSentiment("Very bad", model)
        self.assertEqual(x1 < 0, True)

        x2 = getSentenceSentiment("So good so happy", model)
        self.assertEqual(x2 > 0, True)


if __name__ == '__main__':
    unittest.main()
