# This script is used to prepare everything necessary for the James backend to run
# The intention is that this script is run only once on setup, and then again
#   only if something loaded by this file needs to change

# Library imports
import nltk
import numpy as np
import os
import jdk
import git
import shutil
import stat

# Project imports
from jamesSA import saveSentimentModel
from jamesConfig import sentimentFilename, jamesTrainingData, tempPath, malletPath, apiPath, sentimentPath

# The init method performs all necessary initialization
def init():
    # Set a seed, and load everything necessary from nltk
    np.random.seed(2018)
    nltk.download('wordnet')
    nltk.download('twitter_samples')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    # Build the sentiment model, and save it to a filename imported from jamesConfig,
    #   imported from jamesSA
    if not os.path.exists(sentimentPath()):
        os.mkdir(sentimentPath())
    saveSentimentModel(sentimentFilename(),jamesTrainingData())
    if not os.path.exists(malletPath()):
        git.Git(apiPath()).clone("https://github.com/mimno/Mallet.git")
        os.mkdir(tempPath())
        jdk.install(version="15",path=tempPath())
        git.Git(tempPath()).clone("https://gitbox.apache.org/repos/asf/ant.git")
        os.environ['JAVA_HOME'] = tempPath("jdk")
        os.environ['ANT_HOME'] = tempPath("ant")
        os.environ['PATH'] += os.pathsep + os.path.join(tempPath("ant"),"bin")
        os.system('cd tmp && cd ant && build.bat')
        for root, dirs, files in os.walk(tempPath()):
            for fname in files:
                path = os.path.join(root, fname)
                os.chmod(path ,stat.S_IWRITE)
        os.system('cd Mallet && ant')
        shutil.rmtree(tempPath())
    else: 
        git.cmd.Git(malletPath()).pull()

# Run init
init()
