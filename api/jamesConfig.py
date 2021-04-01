# Library imports
from nltk.corpus import twitter_samples
import os
import sys
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# This file is meant to gather hard-coded names or values, as well as file paths, in one place

cfg = {'topicwords':20,
        'mintokenlen':1,
        'exsnum':5,
        'jdkversion':'15',
        'malletsettings':{'gamma_threshold':0.001,
                          'iterations':50,
                          'random_seed':1},
        'coherencesettings':{'coherence':'c_v'},
        'repo':{'mallet':'https://github.com/mimno/Mallet.git',
                'ant':'https://gitbox.apache.org/repos/asf/ant.git'},
        'path':{'api':os.path.dirname(__file__),
                'pn': [os.path.join(os.path.dirname(__file__),'model','SAmodel'),["api//pos_neg//trainingdata//amazon_cells_labelled.txt","api//pos_neg//trainingdata//imdb_labelled.txt","api//pos_neg//trainingdata//yelp_labelled.txt"],"txt",2000,55],
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