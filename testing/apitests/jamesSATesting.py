# Library imports
import os
import sys
import unittest
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
# Import the file to be tested
from api.jamesSA import read_file, preprocess_data, train_RNN, load_RNN, getSentenceSentiment, RNN_prediction, reTrainModel, getPredictor
# Other required project imports
from api.jamesConfig import cfg
import pandas as pd

class TestSA(unittest.TestCase):
    def test_read_file(self):
        # Test training data import 
        files = cfg['path']["pn"][1]
        x = read_file(files[0],"txt")
        self.assertEqual(len(x) > 0, True)
        
        y = read_file(files[1],"txt")
        self.assertEqual(len(y) > 0, True)

        z = read_file(files[2],"txt")
        self.assertEqual(len(z) > 0, True)

        files2 = cfg['path']['so'][1]
        w = read_file(files2[0],"csv")
        self.assertEqual(len(w)>0,True)

    def test_preprocess_data(self):
        # test sentiment data preprocessing
        df = pd.DataFrame(columns=["text"])
        x = ['THIS IS ALL CAPS']
        df.loc[0] = x
        ret = preprocess_data(df)
        self.assertEqual(ret.text.values[0] == 'this is all caps', True)

        y = ['12345467again']
        df.loc[0] = y
        ret = preprocess_data(df)
        self.assertEqual(ret.text.values[0] == '12345467again', True)
        w = ['!!!abcd']
        df.loc[0] = w
        ret = preprocess_data(df)
        self.assertEqual(ret.text.values[0] == 'abcd', True)
        z = ['$$$$$$$$']
        df.loc[0] = z
        ret = preprocess_data(df)
        self.assertEqual(len(ret.text.values[0]) == 0, True)




    def test_SentimentModel(self):

        # retrain model
        try:
            reTrainModel("pn",2000,"SAmodel")
        except:
            self.assertEqual(False, True)
        #load training data and classifier
        modelInfo = cfg['path']['pn']
        classifier, tokenizer = getPredictor(modelInfo[0],modelInfo[1], modelInfo[2],modelInfo[3])

        # test the sentiment scoring by making a prediction
        x1 = getSentenceSentiment(classifier,["Very bad"],tokenizer, 55)
        self.assertEqual(x1 < 0.5, True)

        # positive sentiments
        x2 = getSentenceSentiment(classifier,["So good so happy"], tokenizer, 55)
        self.assertEqual(x2 > 0, True)

        x3 = getSentenceSentiment(classifier,["Lovely time great"], tokenizer, 55)
        self.assertEqual(x3 > 0, True)

        x4 = getSentenceSentiment(classifier,["It's amazing so wonderful"], tokenizer, 55)
        self.assertEqual(x4 > 0, True)

        x5 = getSentenceSentiment(classifier,["Truly loved all of it"], tokenizer, 55)
        self.assertEqual(x5 > 0, True)

        # negative sentiments
        x6 = getSentenceSentiment(classifier,["gross awful terrible"], tokenizer, 55)
        self.assertEqual(x6 < 0.5, True)

        x7 = getSentenceSentiment(classifier,["stressed sad boring"], tokenizer, 55)
        self.assertEqual(x7 < 0.5, True)

        x8 = getSentenceSentiment(classifier,["lame ugly and not good"], tokenizer, 55)
        self.assertEqual(x8 < 0.5, True)

        x9 = getSentenceSentiment(classifier,["Not good at all"], tokenizer, 55)
        self.assertEqual(x9 < 0.5, True)

        x10 = getSentenceSentiment(classifier,
            ["Unfittingly and inappropriately laughable"], tokenizer, 55)
        self.assertEqual(x10 < 0.5, True)

        # neutral sentiments
        x11 = getSentenceSentiment(classifier,
            ["this neutral sentance"], tokenizer, 55)
        self.assertEqual(x11 < 0.7, True)

        x11 = getSentenceSentiment(classifier,
            ["nothing no thing or anything"], tokenizer, 55)
        self.assertEqual(x11 < 0.7, True)

        x11 = getSentenceSentiment(classifier,
            ["mcmaster james williams names"], tokenizer, 55)
        self.assertEqual(x11 < 0.7, True)

        x11 = getSentenceSentiment(classifier,
            ["doors chairs air"], tokenizer, 55)
        self.assertEqual(x11 > 0.2, True)

        x11 = getSentenceSentiment(classifier,
            ["this is my project"], tokenizer, 55)
        self.assertEqual(x11 < 0.7, True)

        s = ["This is lexicon based approach, what next you can try is classification based approach where you can apply machine learning classifier trained with pre tagged datasets."]
        x12 = getSentenceSentiment(classifier,
            s, tokenizer, 55)
        self.assertEqual(x12 < 0.7, True)

    def test_loadSentimentModel(self):

        #load training data and classifier
        modelInfo = cfg['path']['pn']
        classifier, tokenizer = getPredictor(modelInfo[0],modelInfo[1], modelInfo[2],modelInfo[3])

        # test the sentiment scoring
        x1 = RNN_prediction(classifier,["Very bad"], tokenizer, 55)
        self.assertEqual(len(x1) >0, True)

        x2 = RNN_prediction(classifier,["So good so happy"], tokenizer, 55)
        self.assertEqual(len(x2) > 0, True)

        x3 = RNN_prediction(classifier,["Lovely time great"], tokenizer, 55)
        self.assertEqual(len(x3) > 0, True)

        x4 = RNN_prediction(classifier,["It's amazing so wonderful"], tokenizer, 55)
        self.assertEqual(len(x4) > 0, True)

        x5 = RNN_prediction(classifier,["Truly loved all of it"], tokenizer, 55)
        self.assertEqual(len(x5) > 0, True)

        x6 = RNN_prediction(classifier,["gross awful terrible"], tokenizer, 55)
        self.assertEqual(len(x6) > 0, True)

        x7 = RNN_prediction(classifier,["stressed sad boring"], tokenizer, 55)
        self.assertEqual(len(x7) > 0, True)

        x8 = RNN_prediction(classifier,["lame ugly and not good"], tokenizer, 55)
        self.assertEqual(len(x8) > 0, True)

        x9 = RNN_prediction(classifier,["Not good at all"], tokenizer, 55)
        self.assertEqual(len(x9) > 0, True)

        x10 = RNN_prediction(classifier,[
            "Unfittingly and inappropriately laughable"], tokenizer, 55)
        self.assertEqual(len(x10) > 0, True)

        # neutral sentiments
        x11 = RNN_prediction(classifier,[
            "this neutral sentance"], tokenizer, 55)
        self.assertEqual(len(x11) > 0, True)

        x11 = RNN_prediction(classifier,[
            "dog with a cat and a horse"], tokenizer, 55)
        self.assertEqual(len(x11) > 0, True)

        x11 = RNN_prediction(classifier,[
            "mcmaster james williams names"], tokenizer, 55)
        self.assertEqual(len(x11) > 0, True)

        x11 = RNN_prediction(classifier,[
            "doors chairs and houses and standing"], tokenizer, 55)
        self.assertEqual(len(x11) > 0, True)

        x11 = RNN_prediction(classifier,[
            "this is my project"], tokenizer, 55)
        self.assertEqual(len(x11) > 0, True)

        s = ["This is lexicon based approach, what next you can try is classification based approach where you can apply machine learning classifier trained with pre tagged datasets."]
        x12 = RNN_prediction(classifier,
            s, tokenizer, 55)
        self.assertEqual(len(x12) > 0, True)


if __name__ == '__main__':
    unittest.main()
