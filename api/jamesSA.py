# Library imports
import pickle
import random

from nltk import NaiveBayesClassifier

from jamesConfig import jamesTrainingData
# Project imports
from jamesPreProcessing import jamesLemmatize


# This method is used to build the sentiment analsysis model
# This is called only by saveSentimentModel, found below; the sentiment analysis model can be built and saved,
#	then loaded whenever it is needed, rather than built new each time
# Output: an nltk NaiveBayesClassifier
def buildSentimentModel():
    # Load the jamesTrainingData from jamesConfig, then prepare it for the classifier
    #	using prepareTrainingData, found below
    trainingData = prepareTrainingData(jamesTrainingData())
    # Train a NaiveBayesClassifier, imported from nltk, on the prepared training data
    classifier = NaiveBayesClassifier.train(trainingData)
    # Return the trained NaiveBayesClassifier
    return classifier


# This method is used to prepare training data for an nltk NaiveBayesClassifier
# It is used only by the buildSentimentModel method above
# Input: a dictionary where each key is a label, and each value is the data with this label
# Output: a list of (token, label) pairs, where the tokens and labels are both strings, ready
#	to be used to train a NaiveBayesClassifier
def prepareTrainingData(data):
    # Initialize object to be returned
    trainingData = []
    # Iterate through each label in the input data
    for label in data:
        # Initialize the token list to build
        tokens = []
        # Iterate through each token in the data for the current label, lemmatize the token using
        #	jamesLemmatize, imported from jamesPreProcessing, and append the lemmatized token
        #	to the tokens list
        for token in data[label]:
            tokens.append(jamesLemmatize(token, minTokenLen=1, isTokenized=True, doStem=False, doStemDic=False))
        # Prepare a token dictionary from the lemmatized token list using getTokenDic, found below
        tokenDic = getTokenDic(tokens)
        # Pair each token from the token dictionary with the current label to prepare the dataset
        dataset = [(token, label) for token in tokenDic]
        # Add this dataset to the set of training data to be returned
        trainingData += dataset
    # Once every label set is added, shuffle the training data
    random.shuffle(trainingData)
    # Return the prepared training data
    return trainingData


# This is a helper method used to prepare the token dictionary for training data
# It is only used by the prepareTrainingData method above
# Input: a list of token lists
# Output: a list of dictionaries, where each key is a token from the input
#	list, and each value is True
def getTokenDic(tokenList):
    for tokens in tokenList:
        yield dict([token, True] for token in tokens)


# This method builds a sentiment model, and saves it to a specified filename
# It is called only by init, as the sentiment model only needs to be built and
#	saved on setup
# Input: the filename to save to as a string
def saveSentimentModel(filename):
    # Build the sentiment model using the buildSentimentModel method above
    sentimentModel = buildSentimentModel()
    # Save the sentiment model using pickle, to the specified filename
    f = open(filename, "wb")
    pickle.dump(sentimentModel, f)
    f.close()
    return


# This method loads a saved sentiment model and returns it
# This is called in jamesMain to run sentiment analysis
# Output: an nltk NaiveBayesClassifier
def loadSentimentModel(filename):
    # Load the sentiment model using pickle, and return it
    f = open(filename, "rb")
    sentimentModel = pickle.load(f)
    f.close()
    return sentimentModel


# This method uses a sentiment analysis model to find the probability that
#	a given sentence is positive
# Input: the sentence as a string, and a NaiveBayesClassifier sentiment analysis model
# Output: the probability that the given sentence is positive as a float
def getSentenceSentiment(text, model):
    # Lemmatize the given sentence using jamesLemmatize, imported from jamesPreProcessing
    tokens = jamesLemmatize(text, minTokenLen=1, isTokenized=False, doStem=False, doStemDic=False)
    # Use the given NaiveBayesClassifier to classify the sentence
    results = model.prob_classify(dict([token, True] for token in tokens))
    # Return the probability that the sentence was positive
    return results.prob('Positive')
