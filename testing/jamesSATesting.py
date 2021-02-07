from api.jamesSA import buildSentimentModel, prepareTrainingData, getTokenDic, saveSentimentModel, loadSentimentModel, getSentenceSentiment
from api.jamesConfig import jamesTrainingData
import unittest


class TestSA(unittest.TestCase):
    def test_prepareTrainingData(self):
        data1 = jamesTrainingData()
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
        data = jamesTrainingData()
        self.assertEqual(isinstance(data, dict), True)

        # train a classifier
        classifier = buildSentimentModel(jamesTrainingData())

        # save the classifier to file
        saveSentimentModel("testSAModel.pickle", jamesTrainingData())

        # test the sentiment scoring by making a prediction
        x1 = getSentenceSentiment("Very bad", classifier)
        self.assertEqual(x1 < 0, True)

        x2 = getSentenceSentiment("So good so happy", classifier)
        self.assertEqual(x2 > 0, True)

    def test_loadSentimentModel(self):
        # load a model
        model = loadSentimentModel("testSAModel.pickle")

        # test the sentiment scoring
        x1 = getSentenceSentiment("Very bad", model)
        self.assertEqual(x1 < 0, True)

        x2 = getSentenceSentiment("So good so happy", model)
        self.assertEqual(x2 > 0, True)


if __name__ == '__main__':
    unittest.main()
