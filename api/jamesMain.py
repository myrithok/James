# Library imports
import os
import sys
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Project imports
from api.jamesClasses import docResults, jamesResults
from api.jamesConfig import cfg
from api.jamesLDA import buildCoherenceModel, buildTopicModel, getResults, getTopics
from api.jamesPreProcessing import preProcess, preProcessSentence
from api.jamesSA import getPredictor, getSentenceSentiment

def process(inputCorpus, topicNum, datasetChoice):
    '''
    Main method called by server.py to handle processing of input corpus

    Parameters
    ----------
            inputCorpus: inputCorpus
                    the corpus uploaded by the user as an inputCorpus object (imported
                    from jamesClasses)

            topicNum: int
                    the number of topics to be generated by the topic model, provided by the user

    Output
    ------
            dict
                    the result set as a dictionary containing nested dictionaries, to be easily
                    converted to a json object
    '''
    # Pre process input corpus using preProcess method imported from jamesPreProcessing
    # Input is inputCorpus object, imported from jamesClasses
    # Output is jamesCorpus object, imported from jamesClasses
    corpus = preProcess(inputCorpus)
    # Raise an error if the input text is too short for the number of topics
    assert len(corpus.dic) > topicNum, "Input is too short for number of selected topics"
    # Load the user-selected sentiment model using getPredictor, imported from jamesSA
    modelInfo = cfg['path'][datasetChoice]
    sentimentmodel, tokenizer = getPredictor(modelInfo[0],modelInfo[1], modelInfo[2],modelInfo[3])
    # Build the topic model on the corpus using the input number of topics
    topicModel = buildTopicModel(corpus, topicNum)
    # Build the coherence model for generated topic model
    coherenceModel = buildCoherenceModel(topicModel, corpus)
    # Produce a jamesResults object, imported from jamesClasses, containing the topic
    #   model information using getResults, imported from jamesLDA
    results = getResults(topicModel, coherenceModel, corpus)
    # Add the stem dictionary produced in preprocessing to the jamesResults object
    # Words are stemmed for topic modeling, but a dictionary is kept mapping each stem
    #   to a word converted to that stem, which is used to make results more readable
    results.addStemDic(corpus.stemDic)
    # Iterate through each document in the corpus for analysis
    for doc in corpus.docs:
        # Construct a docResults object, imported from jamesClasses, containing the topic
        #   breakdown compared to the constructed topic model for the document in question
        #   produced by getTopics, imported from jamesLDA
        docResult = docResults(doc.title, getTopics(doc.bow, topicModel))
        # Iterate through each sentence in the document for sentiment analysis
        for sentence in doc.sentences:
            # Preprocess the sentence for topic modeling
            processedSentence = preProcessSentence(sentence, corpus.dic)
            # Use the constructed topic model to find the topic distribution for the
            #   current sentence using getTopics, imported from jamesLDA
            sentenceTopics = getTopics(processedSentence, topicModel)
            # Check to see if this sentence would be a good example sentence for any
            #    topic, and add this sentence to the topic if so
            results.addSentence(sentence, sentenceTopics)
            # Use the sentiment analysis model to find the sentiment for the current
            #   sentence using getSentenceSentiment, imported from jamesSA
            sentenceSentiment = getSentenceSentiment(sentimentmodel, [sentence], tokenizer, modelInfo[4])
            # Add the sentence's sentiment to each topic's sentiment for the current
            #   document results docResults object, weighted by the sentence's topic
            #   distribution
            for topic in sentenceTopics:
                docResult.addSentiment(topic[0], topic[1], sentenceSentiment)
        # Calculate the average sentiment for each topic in the current document
        docResult.averageSentiments()
        # Add the docResults object to the jamesResults result set
        results.addDocResults(docResult)
    # Use the jamesResults output method to output results as nested dictionaries
    #   and lists, which can be converted to a json object
    return results.output()
