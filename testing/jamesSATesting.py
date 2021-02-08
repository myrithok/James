from api.jamesSA import buildSentimentModel, prepareTrainingData, getTokenDic, saveSentimentModel, loadSentimentModel, getSentenceSentiment
from api.jamesConfig import jamesTrainingData
import unittest


class TestSA(unittest.TestCase):
    def test_prepareTrainingData(self):
        # Test training data import and prepare
        data1 = jamesTrainingData()
        self.assertEqual(isinstance(data1, dict), True)

        ret = prepareTrainingData(data1)
        self.assertEqual(isinstance(ret, list), True)

    def test_getTokenDic(self):
        # test tokenization dictionary conversion
        tokenList = ["test", "case"]
        x = getTokenDic(tokenList)
        for token in x:
            self.assertEqual(isinstance(token, dict), True)

        tokenList = ["token1", "token2", "token3"]
        x = getTokenDic(tokenList)
        for token in x:
            self.assertEqual(isinstance(token, dict), True)

        tokenList = [""]
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

        # positive sentiments
        x2 = getSentenceSentiment("So good so happy", classifier)
        self.assertEqual(x2 > 0, True)

        x3 = getSentenceSentiment("Lovely time great", classifier)
        self.assertEqual(x3 > 0, True)

        x4 = getSentenceSentiment("It's amazing so wonderful", classifier)
        self.assertEqual(x4 > 0, True)

        x5 = getSentenceSentiment("Truly loved all of it", classifier)
        self.assertEqual(x5 > 0, True)

        # negative sentiments
        x6 = getSentenceSentiment("gross awful terrible", classifier)
        self.assertEqual(x6 < 0, True)

        x7 = getSentenceSentiment("stressed sad boring", classifier)
        self.assertEqual(x7 < 0, True)

        x8 = getSentenceSentiment("lame ugly and not good", classifier)
        self.assertEqual(x8 < 0, True)

        x9 = getSentenceSentiment("Not good at all", classifier)
        self.assertEqual(x9 < 0, True)

        x10 = getSentenceSentiment(
            "Unfittingly and inappropriately laughable", classifier)
        self.assertEqual(x10 < 0, True)

        # neutral sentiments
        x11 = getSentenceSentiment(
            "this neutral sentance", classifier)
        self.assertEqual(x11 < 0.5, True)

        x11 = getSentenceSentiment(
            "dog with a cat and a horse", classifier)
        self.assertEqual(x11 < 0.5, True)

        x11 = getSentenceSentiment(
            "mcmaster james williams names", classifier)
        self.assertEqual(x11 < 0.5, True)

        x11 = getSentenceSentiment(
            "doors chairs and houses and standing", classifier)
        self.assertEqual(x11 < 0.5, True)

        x11 = getSentenceSentiment(
            "this is my project", classifier)
        self.assertEqual(x11 < 0.5, True)

        s = "This is lexicon based approach, what next you can try is classification based approach where you can apply machine learning classifier trained with pre tagged datasets."
        x12 = getSentenceSentiment(
            s, classifier)
        self.assertEqual(x12 < 0.5, True)

    def test_loadSentimentModel(self):
        # load a model
        classifier = loadSentimentModel("testSAModel.pickle")

        # test the sentiment scoring
        x1 = getSentenceSentiment("Very bad", classifier)
        self.assertEqual(x1 < 0, True)

        x2 = getSentenceSentiment("So good so happy", classifier)
        self.assertEqual(x2 > 0, True)

        x3 = getSentenceSentiment("Lovely time great", classifier)
        self.assertEqual(x3 > 0, True)

        x4 = getSentenceSentiment("It's amazing so wonderful", classifier)
        self.assertEqual(x4 > 0, True)

        x5 = getSentenceSentiment("Truly loved all of it", classifier)
        self.assertEqual(x5 > 0, True)

        x6 = getSentenceSentiment("gross awful terrible", classifier)
        self.assertEqual(x6 < 0, True)

        x7 = getSentenceSentiment("stressed sad boring", classifier)
        self.assertEqual(x7 < 0, True)

        x8 = getSentenceSentiment("lame ugly and not good", classifier)
        self.assertEqual(x8 < 0, True)

        x9 = getSentenceSentiment("Not good at all", classifier)
        self.assertEqual(x9 < 0, True)

        x10 = getSentenceSentiment(
            "Unfittingly and inappropriately laughable", classifier)
        self.assertEqual(x10 < 0, True)

        # neutral sentiments
        x11 = getSentenceSentiment(
            "this neutral sentance", classifier)
        self.assertEqual(x11 < 0.5, True)

        x11 = getSentenceSentiment(
            "dog with a cat and a horse", classifier)
        self.assertEqual(x11 < 0.5, True)

        x11 = getSentenceSentiment(
            "mcmaster james williams names", classifier)
        self.assertEqual(x11 < 0.5, True)

        x11 = getSentenceSentiment(
            "doors chairs and houses and standing", classifier)
        self.assertEqual(x11 < 0.5, True)

        x11 = getSentenceSentiment(
            "this is my project", classifier)
        self.assertEqual(x11 < 0.5, True)

        s = "This is lexicon based approach, what next you can try is classification based approach where you can apply machine learning classifier trained with pre tagged datasets."
        x12 = getSentenceSentiment(
            s, classifier)
        self.assertEqual(x12 < 0.5, True)


if __name__ == '__main__':
    unittest.main()
