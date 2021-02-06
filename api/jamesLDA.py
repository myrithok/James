# Library imports
from gensim.models import wrappers, coherencemodel
import os

# Project imports
from jamesClasses import jamesResults
from jamesConfig import cfg

def buildTopicModel(corpus, topicNum):
    '''
    This method is used to build a gensim topic model of the given number of
    topics for a given corpus. If a number is not specified, then the
    buildBestCoherenceTopicModel function is called. If a number is specified,
    then buildMalletModel is called. Both of these functions return a mallet model,
    which is converted to a gensim lda model and returned.

                    buildTopicModel
                        |    |
    (topicNum specified)|    |(topicNum not specified)
                        |    |________________
                        |                     |
                        |                     V
                  (once)|        buildBestCoherenceTopicModel
                        |        _____________|
                        |       |      (multiple times)
                        V       V
                     buildMalletModel

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
    # If the number of topics is no specified, call buildBestCoherenceTopicModel
    if topicNum == None:
        ldaMallet = buildBestCoherenceTopicModel(corpus)
    # If the number of of topics is specified, build a mallet model with that many topcis
    else: 
        ldaMallet = buildMalletModel(corpus, topicNum)
    # convert the ldaMallet model to an ldaModel
    ldaModel = wrappers.ldamallet.malletmodel2ldamodel(ldaMallet, gamma_threshold=0.001, iterations=50)
    # Return the topic model
    return ldaModel

def buildBestCoherenceTopicModel(corpus):
    '''
    This method is used to the ideal number of topics for a topic model when
    a number is not specified by the user
    This is done by building a topic model using buildMalletModel for each number of
    topics between 2 and a maximum, then picking the topic model from these that had
    the highest average coherence score for its topics

    Parameters
    ----------
            corpus: jamesCorpus
                    the corpus to be modeled, as a jamesCorpus
                    object (imported from jamesClasses)

    Output
    ------
            gensim.models.wrappers.LdaMallet
                    the topic model generated from the input corpus
    '''
    # Import the maximum number of topics to try from jamesConfig
    maximum = cfg['topicmax']
    # Initialize each variable to test the max
    topScore = topModel = currentModel = currentResults = currentScore = None
    # save the results coherence scores to a list for verification
    scores = []
    # Iterate through each number of topics to try, between 2 and the maximum (inclusive)
    for n in range(2, maximum + 1):
        # Build the topic model for the current number of topics using buildTopicModel found above
        currentModel = buildMalletModel(corpus,n)
        ### run CoherenceModel for each new Mallet Model. Requires getLemmatized() which was added method
        ### using coherence method "c_v" allows for results between (0,1) where greater number is better score
        currentCoherence = coherencemodel.CoherenceModel(model=currentModel, texts=corpus.getLemmatized(),
                                                         dictionary=corpus.dic, corpus=corpus.getBoW(),
                                                         coherence="c_v")
        currentScore = currentCoherence.get_coherence()
        scores.append(currentScore)
        # If this model has a higher average coherence score than the current best,
        #   or it is the first model generated, store this model and score as the
        #   top model and score
        if topScore == None or currentScore > topScore:
            topScore = currentScore
            topModel = currentModel
    # Return the top model that was found
    return topModel

def buildMalletModel(corpus, topicNum):
    '''
    This method is used to build a mallet lda model.
    It is called once by buildTopicModel if a number of topics has been specified,
    or several times by buildBestCoherenceTopicModel to find the best coherence
    score if no number of topics was specified.

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
    return jamesResults(topicModel.top_topics(corpus.getBoW()))

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
