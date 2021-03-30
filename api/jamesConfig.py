# Library imports
from nltk.corpus import twitter_samples
import os
import sys
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# This file is meant to gather hard-coded names or values, as well as file paths, in one place

cfg = {'topicmax':20,
        'topicwords':20,
        'mintokenlen':1,
        'exsnum':3,
        'jdkversion':'15',
        'satraining':{"Positive": twitter_samples.tokenized('positive_tweets.json'),
                      "Negative": twitter_samples.tokenized('negative_tweets.json')},
        'repo':{'mallet':'https://github.com/mimno/Mallet.git',
                'ant':'https://gitbox.apache.org/repos/asf/ant.git'},
        'path':{'api':os.path.dirname(__file__),
                'sapath':os.path.join(os.path.dirname(__file__),'model'),
                'safile':os.path.join(os.path.dirname(__file__),'model','jamesSentimentModel.pickle'),
                'pn': [os.path.join(os.path.dirname(__file__),'model','SAmodel'),["trainingdata//amazon_cells_labelled.txt","trainingdata//imdb_labelled.txt","trainingdata//yelp_labelled.txt"],"txt",2000,55],
                'so': [os.path.join(os.path.dirname(__file__),'model','SOmodel'),["api//trainingdata//convote_v1.1//SO_congressional_data.csv"],"csv",500,91],
                'malletpath':os.path.join(os.path.dirname(__file__),'Mallet'),
                'malletfile':os.path.join(os.path.dirname(__file__),'Mallet','bin','mallet'),
                'malletlogging':os.path.join(os.path.dirname(__file__),'Mallet','src','cc','mallet','util','resources','logging.properties'),
                'tmp':os.path.join(os.path.dirname(__file__),'tmp'),
                'antpath':os.path.join(os.path.dirname(__file__),'tmp','ant'),
                'antfile':os.path.join(os.path.dirname(__file__),'tmp','ant','dist'),
                'antbin':os.path.join(os.path.dirname(__file__),'tmp','ant','dist','bin')},
        'host':{'ip':'0.0.0.0',
                'port':8002}
}