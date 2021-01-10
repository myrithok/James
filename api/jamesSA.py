from jamesPreProcessing import saPreProcess
from nltk.tag import pos_tag
from nltk.corpus import twitter_samples
from nltk import classify, NaiveBayesClassifier
import random
import pickle
import jamesConfig

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def buildSentimentModel():
	positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
	negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
	positive_cleaned_tokens_list = []
	negative_cleaned_tokens_list = []
	for tokens in positive_tweet_tokens:
	    positive_cleaned_tokens_list.append(saPreProcess(tokens))
	for tokens in negative_tweet_tokens:
	    negative_cleaned_tokens_list.append(saPreProcess(tokens))
	positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
	negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)
	positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]
	negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]
	dataset = positive_dataset + negative_dataset
	random.shuffle(dataset)
	train_data = dataset
	classifier = NaiveBayesClassifier.train(train_data)
	return classifier

def loadSentimentModel():
	f = open(jamesConfig.sentimentFilename(),"rb")
	sentimentModel = pickle.load(f)
	f.close()
	return sentimentModel

def getSentenceSentiment(text, model):
	custom_tokens = saPreProcess(text)
	results = model.prob_classify(dict([token, True] for token in custom_tokens))
	return results.prob('Positive')