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
import time

# Project imports
from jamesSA import saveSentimentModel
from jamesConfig import cfg

# The init method performs all necessary initialization
def init():
    print("Beginning setup...")
    # Set a seed, and load everything necessary from nltk
    print("Downloading nltk data...")
    np.random.seed(2018)
    nltk.download('wordnet')
    nltk.download('twitter_samples')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    # Create the model folder if it does not already exist
    if not os.path.exists(cfg['path']['sapath']):
        print("Creating model folder...")
        os.mkdir(cfg['path']['sapath'])
    # Build the sentiment model and save it, overwriting any existing model
    #    Imported from jamesSA
    print("Generating sentiment model...")
    saveSentimentModel(cfg['path']['safile'],cfg['satraining'])
    # If the mallet folder does not already exist, perform first time setup
    if not os.path.exists(cfg['path']['malletpath']):
        # Clone the latest mallet repo
        print("Cloning mallet repo...")
        git.Git(cfg['path']['api']).clone(cfg['repo']['mallet'])
        # Edit mallet logging settings to suppress console output
        print("Suppressing mallet console output...")
        file = open(cfg['path']['malletlogging'],'r')
        logging = file.read()
        file.close()
        logging = logging.replace(".level= INFO", ".level= SEVERE")
        file = open(cfg['path']['malletlogging'],'w')
        file.write(logging)
        file.close()
        # Create a temp folder for temporary setup software
        print("Creating temp folder...")
        os.mkdir(cfg['path']['temp'])
        # Install latest JDK using the AdoptOpenJDK API into the temp folder
        print("Installing JDK...")
        jdk.install(version=cfg['jdkversion'],path=cfg['path']['temp'])
        # Clone the latest Apache ant repo into the temp folder
        print("Cloning ant repo...")
        git.Git(cfg['path']['temp']).clone(cfg['repo']['ant'])
        # Disable the read-only property of all files in the temp folder
        # Several files in these repos may be marked as read-only by default,
        #    which must be disabled for these files to be cleaned up at the end
        print("Disabling read-only...")
        for root, dirs, files in os.walk(cfg['path']['temp']):
            for fname in files:
                path = os.path.join(root, fname)
                os.chmod(path ,stat.S_IWRITE)
        time.sleep(5)
        # Build apache ant
        print("Building ant...")
        os.environ['JAVA_HOME'] = os.path.join(cfg['path']['temp'],[ f.name for f in os.scandir("tmp") if f.is_dir() and f.name.startswith("jdk") ][0])
        os.environ['ANT_HOME'] = cfg['path']['antfile']
        os.environ['PATH'] += os.pathsep + cfg['path']['antbin']
        os.system('cd ' + cfg['path']['antpath'] + ' && build.bat')
        # Build mallet
        print("Building mallet...")
        os.system('cd ' + cfg['path']['malletpath'] + ' && ant')
        # Delete the temp folder and all contents
        print("Cleaning up temp folder...")
        shutil.rmtree(cfg['path']['temp'])
    # If the mallet folder already exists, then pull the mallet repo to ensure
    #    it is up-to-date
    else:
        print("Pulling latest mallet...")
        git.cmd.Git(cfg['path']['malletpath']).pull()
    print("Setup complete")

# Run init
init()
