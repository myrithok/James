# Library imports
from gensim.models import wrappers, coherencemodel
import os
import sys
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Project imports
from api.jamesClasses import jamesResults
from api.jamesConfig import cfg

def buildTopicModel(corpus, topicNum):
    '''
    This method is used to build a gensim topic model of the given number of
    topics for a given corpus. 

    Parameters
    ----------
            corpus: jamesCorpus
                    the corpus to be modeled, as a jamesCorpus
                    object (imported from jamesClasses)

            topicNum: int
                    the number of topics to generate

    Output
    ------
            gensim.models.ldamodel
                    the topic model generated from the input corpus
    '''
    # Build a mallet model with that many topcis
    ldaMallet = buildMalletModel(corpus, topicNum)
    # convert the ldaMallet model to an ldaModel
    ldaModel = wrappers.ldamallet.malletmodel2ldamodel(ldaMallet,
                                                       gamma_threshold=cfg['malletsettings']['gamma_threshold'],
                                                       iterations=cfg['malletsettings']['iterations'])
    # Return the topic model
    return ldaModel

def buildMalletModel(corpus, topicNum):
    '''
    This method is used to build a mallet lda model.
    It is called by buildTopicModel.

    Parameters
    ----------
            corpus: jamesCorpus
                    the corpus to be modeled, as a jamesCorpus
                    object (imported from jamesClasses)

            topicNum: int
                    the number of topics to generate

    Output
    ------
            gensim.models.wrappers.LdaMallet
                    the topic model generated from the input corpus
    '''
    #Add the path to mallet, imported from jamesConfig, to the environment
    os.environ['MALLET_HOME'] = cfg['path']['malletpath']
    # Build the topic model for the given number of topics using mallet, importedd
    #    from the gensim library 
    malletModel = wrappers.LdaMallet(cfg['path']['malletfile'], corpus=corpus.getBoW(), num_topics=topicNum, id2word=corpus.dic,
                                       random_seed=1)
    # Return the constructed mallet model
    return malletModel

def getResults(topicModel, corpus):
    '''
    This method is used to construct a jamesResults object (imported from jamesClasses)
    containing the topic results of a given topic model and corpus

    Parameters
    ----------
            topicModel: gensim.models.ldamodel
                    the topic model whose results are being returned

            corpus: jamesCorpus
                    the corpus used to generate the input topic model as a
                    jamesCorpus object (imported from jamesClasses)

    Output
    ------
            jamesResults
                    a jamesResults object (imported from jamesClasses) containing
                    the topic results
    '''
    return jamesResults(topicModel.top_topics(corpus.getBoW(),topn=cfg['topicwords']))

def getTopics(bow, topicModel):
    '''
    This method is used to find the topic distribution of a given document or sentence
    It is used by jamesMain to find the topic distribution of documents for the result set,
    and to find the topic distribution of each sentence for sentiment weighting

    Parameters
    ----------
            bow: list
                    a preprocessed bag of words to be checked against the topic model

            topicModel: gensim.models.ldamodel
                    the topic model being used to check the topics of a bag of words

    Output
    ------
            list
                    the topic distribution as a list of (topic number, weight) pairs, where
                    the topic number is an integer, and the weight is a float
    '''
    return topicModel.get_document_topics(bow, 0.0)
