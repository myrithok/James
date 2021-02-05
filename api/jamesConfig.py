# Library imports
import os
from nltk.corpus import twitter_samples
# This file is meant to gather hard-coded names or values, as well as file paths, in one place

cfg = {'topicmax':20,
        'jdkversion':'15',
        'satraining':{"Positive": twitter_samples.tokenized('positive_tweets.json'),
                      "Negative": twitter_samples.tokenized('negative_tweets.json')},
        'repo':{'mallet':'https://github.com/mimno/Mallet.git',
                'ant':'https://gitbox.apache.org/repos/asf/ant.git'},
        'path':{'api':os.path.dirname(__file__),
                'sapath':os.path.join(os.path.dirname(__file__),'model'),
                'safile':os.path.join(os.path.dirname(__file__),'model','jamesSentimentModel.pickle'),
                'malletpath':os.path.join(os.path.dirname(__file__),'Mallet'),
                'malletfile':os.path.join(os.path.dirname(__file__),'Mallet','bin','mallet'),
                'temp':os.path.join(os.path.dirname(__file__),'tmp'),
                'antpath':os.path.join(os.path.dirname(__file__),'tmp','ant'),
                'antfile':os.path.join(os.path.dirname(__file__),'tmp','ant','dist'),
                'antbin':os.path.join(os.path.dirname(__file__),'tmp','ant','dist','bin')}
}