# Library imports
import os

# This file is meant to gather hard-coded names or values, as well as file paths, in one place

def sentimentFilename():
    '''
    sentimentFilename returns the name of the saved sentiment analysis model
    This is used to save and load the model by jamesSA

    Output
    ------
            str
                    the filename to save and load the sentiment analysis model
    '''
    return os.path.join(os.path.dirname(__file__),'model','jamesSentimentModel.pickle')

def jamesTopicMaximum():
    '''
    jamesTopicMaximum provides the maximum number of topics to test when testing
    for the number of topics that produces the highest average coherence score
    It is used by jamesLDA

    Output
    ------
            int
                    the maximum number of topics to test when testing for coherence scores
    '''
    return 20

def jamesTrainingData():
    '''
    jamesTrainingData provides the training data source for the sentiment analysis model
    It is used by init

    Output
    ------
            dict
                    training data for the sentiment analysis model as a dictionary
                    where each key is a label, and the associated value is the data
                    with that label
    '''
    from nltk.corpus import twitter_samples
    return {"Positive": twitter_samples.tokenized('positive_tweets.json'),
            "Negative": twitter_samples.tokenized('negative_tweets.json')}



def malletPath():
    '''
    malletPath provides the path to the mallet model folder
    It is used by jamesLDA

    Output
    ------
            str
                    the path to the mallet folder
    '''
    return os.path.join(os.path.dirname(__file__),'Mallet')

def malletFile():
    '''
    malletFile provides the path to the mallet file within the mallet folder
    It is used by jamesLDA

    Output
    ------
            str
                    the path to the mallet file
    '''
    return os.path.join(malletPath(),'bin','mallet')

def tempPath(dir = None):

    if dir == None:
        return os.path.join(os.path.dirname(__file__),'tmp')
    if dir == "ant":
        return os.path.join(os.path.dirname(__file__),'tmp',"ant","dist")
    if dir == "antbuild":
        return os.path.join(os.path.dirname(__file__),'tmp',"ant")
    elif dir == "jdk":
        return os.path.join(os.path.dirname(__file__),'tmp',[ f.name for f in os.scandir("tmp") if f.is_dir() and f.name.startswith("jdk") ][0])

def apiPath():

    return os.path.dirname(__file__)

def sentimentPath():
    return os.path.join(os.path.dirname(__file__),'model')