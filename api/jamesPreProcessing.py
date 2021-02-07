# Library imports
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.tag import pos_tag
import re
import string

# Project imports
from api.jamesClasses import jamesCorpus, inputCorpus, corpusDoc


def preProcess(corpus):
    '''
    This method handles all preprocessing for the input corpus to prepare it for analysis
    It is used by jamesMain

    Parameters
    ----------
            corpus: inputCorpus
                    the corpus to be preprocessed, as an inputCorpus object (imported
                    from jamesClasses)

    Output
    ------
            jamesCorpus
                    the processed corpus, as a jamesCorpus object (imported from
                    jamesClasses)
    '''
    # Get the corpusDoc list from the inputCorpus (both imported from jamesClasses)
    docs = corpus.docs
    # Initialize objects to hold a list of lemmatized document and a stem dictionary
    lemmatizedList = []
    stemDic = {}
    # Iterate through each corpusDoc (imported from jamesClasses) for preprocessing
    for doc in docs:
        # Separate the document into a list of sentences using the separateSentences method
        #   (found below), and add this list to the corpusDoc object (imported from jamesClasses)
        # This list will be used to iterate through each sentence for topic modeling and sentiment
        #   analysis later
        doc.addSentences(separateSentences(doc.text))
        # Lemmatize the document using jamesLemmatize (found below)
        lemmatized = jamesLemmatize(doc.text, minTokenLen=4, doStem=True, doStemDic=True)
        # Add the lemmatized document stem list to the corpusDoc (imported from jamesClasses),
        #   to be used to generate the document's word id bag of words
        doc.addLemmatized(lemmatized["lemmatized"])
        # Also add the lemmatized document stem list to the lemmatized list, to be used
        #   to construct the stem id dictionary
        lemmatizedList.append(lemmatized["lemmatized"])
        # Update the stem dictionary with the lemmatized document stem dictionary
        stemDic.update(lemmatized["stemDic"])
    # Construct a word stem id dictionary from the list of lemmatized documents using
    # Dictionary, imported from gensim.corpora
    dic = Dictionary(lemmatizedList)
    # Iterate through each document to generate a bag of word ids using the lemmatized
    #   document and the word stem id dictionary, and add that bag of word ids to
    #   the corpusDoc object(imported from jamesClasses)
    for doc in docs:
        doc.addBoW(dic.doc2bow(doc.lemmatized))
    # Construct a jamesCorpus object (imported from jamesClasses) with the list of
    #   corpusDoc objects, the word stem id dictionary, and the stem word dictionary,
    #   and return it
    return jamesCorpus(docs, dic, stemDic)

def preProcessSentence(text, dic):
    '''
    This method is used to preprocess individual sentences for topic modeling

    Parameters
    ----------
            text: str
                    the sentenced to be processed, as a string

            dic: gensim.corpora.Dictionary
                    a dicitionary mapping word stem ids to word stems

    Output
    ------
            list
                    the sentence represented as a list of (word id, index) pairs,
                    where word id and index are both ints
    '''
    # Lemmatize and stem the sentence using jamesLemmatize (found below),
    #   convert the stem results to a bag of word stem ids, and return it
    return dic.doc2bow(jamesLemmatize(text, minTokenLen=4, doStem=True, doStemDic=False)["lemmatized"])

def jamesLemmatize(tokens, minTokenLen, doStem, doStemDic):
    '''
    This method is used to lemmatize and stem text for both topic modeling and sentiment analysis
    It is used by preProcess and preProcessSentence above, as well as jamesSA

    Parameters
    ----------
            tokens: list or str
                    the input to be lemmatized and stemmed
                    either a string that has not yet been tokenized, or a list representing an
                    already tokenized string

            minTokenLen: int
                    the minimum allowable token length when lemmatizing the input

            doStem: bool
                    a setting for whether or not the input should also be stemmed

            doStemDic: bool
                    a setting for whether or not a word stem to word dictionary should be
                    constructed during lemmatization and returned with the results

    Output
    ------
            dict
                    a dictionary containing the results of lemmatization
                    if doStem and doStemDic are both true, the dictionary will have two keys:
                    "lemmatized" which has a list representing the lemmatized input as a value,
                    and "stemDic" which has the word stem to word dictionary as a value
                    otherwise, the dictionary will have only have the lemmatized key and value
    '''
    # Initialize the objects to be returned, if needed
    lemmatized = []
    if doStemDic:
        stemDic = {}
    # Initialize a WordNetLemmatizer, imported from nltk.stem
    lemmatizer = WordNetLemmatizer()
    # Initialize a SnowballStemmer in english, imported from nltk.stem, if needed
    if doStem:
        stemmer = SnowballStemmer('english')
    # Tokenize the text using simple_preprocess, imported from gensim.utils, if needed
    if type(tokens) == str:
        tokens = simple_preprocess(tokens)
    # Tag each word using pos_tag, imported from nltk.tag, and iterate through each token and tag
    for token, tag in pos_tag(tokens):
        # Filter out undesired information from the token, and format it to lowercase
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)
        token = token.lower()
        # Check whether the token is tagged as a noun, a verb, or other, and set pos appropriately
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        # Filter out each token that is punctuation, in STOPWORDS (imported from
        #   gensim.parsing.preprocessing), or is shorter than the minimum acceptable token length
        if token not in STOPWORDS and token not in string.punctuation and len(token) >= minTokenLen:
            # Lemmatize the token using WordNetLemmatizer
            lemma = lemmatizer.lemmatize(token, pos)
            # Stem the token using the SnowballStemmer, if needed
            if doStem:
                lemma = stemmer.stem(lemma)
                # Add the the stem to the stem dictionary as a key with a value of the lemma which produced
                #   the stem if the stem is not already in the stem dictionary, and if a stem dictionary
                #   is needed
                if doStemDic:
                    if lemma not in stemDic:
                        stemDic[lemma] = token
            # Add the lemma to the lemmatized list
            lemmatized.append(lemma)

    # If a stem dictionary is required, return a dictionary containing the stems list and stem dictionary
    if doStemDic:
        return {"lemmatized": lemmatized, "stemDic": stemDic}
    # Otherwise, return a dictionary with only the lemmatized list
    return {"lemmatized": lemmatized}

def separateSentences(text):
    '''
    This method is used to separate a document into a clean list of sentences

    Parameters
    ----------
            text: str
                    the document to be separated

    Output
    ------
            list
                    a list of strings, where each string is a sentence from the document
    '''
    if not isinstance(text, str):
        raise TypeError
    # Add a newline after every period, exclamation point, and question mark
    text = text.replace(".", ".\n")
    text = text.replace("!", "!\n")
    text = text.replace("?", "?\n")
    # Split the text into a list of strings on every newline
    # This should include newlines in the original text, as well as newlines
    #   that were added after every period, exclamation point, and question mark
    sentences = text.split("\n")
    # Strip leading and trailing whitespace from every sentence in the list, and filter
    #   the resulting sentences using sentenceFilter found below
    cleaned = filter(sentenceFilter, [sentence.strip() for sentence in sentences])
    # Convert the results back to a list, and return them
    return list(cleaned)

def sentenceFilter(sentence):
    '''
    This method is used as a filter for the filter method used in separateSentences above,
    using a regular expression search imported from re

    Parameters
    ----------
            sentence: str
                    the sentence as a string

    Output
    ------
            bool
                    true if the sentence contains at least one letter, false otherwise
    '''
    if not isinstance(sentence, str):
        raise TypeError
    if re.search('[a-zA-Z]', sentence):
        return True
    return False
