from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer, PorterStemmer
from nltk.tag import pos_tag
import re, string
from jamesClasses import jamesCorpus

#This section prepares the input for topic modeling
def preProcess(corpus):
	docs = corpus.docs
	lemmatizedList = []
	for doc in docs:
		doc.addSentences(separateSentences(doc.text))
		lemmatized = preLemmatize(doc.text)
		doc.addLemmatized(lemmatized)
		lemmatizedList.append(lemmatized)
	dic = Dictionary(lemmatizedList)
	for doc in docs:
		doc.addBoW(dic.doc2bow(doc.lemmatized))
	return jamesCorpus(docs,dic)

def preProcessSentence(text,dic):
	return dic.doc2bow(preLemmatize(text))

def preStemming(text):
	stemmer = PorterStemmer()
	return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preLemmatize(text):
    result = []
    for token in simple_preprocess(text):
        if token not in STOPWORDS and len(token) > 3:
            result.append(preStemming(token))
    return result

#This section separates and cleans sentences for iteration
def separateSentences(data):
	text = data.replace("\n","")
	sentences = text.split(".")
	cleaned = map(sentenceCleaner,sentences)
	cleaned = filter(sentenceFilter,cleaned)
	return list(cleaned)

def sentenceFilter(sentence):
	if re.search('[a-zA-Z]', sentence):
		return True
	return False

def sentenceCleaner(sentence):
	sentence = sentence + "."
	if sentence[0] == " ":
		sentence = sentence[1:]
	return sentence

#This section handles preprocessing for sentiment analysis
def saPreProcess(tokens):
	cleaned_tokens = remove_noise(tokens)
	lemmatizer = WordNetLemmatizer()
	lemmatized_sentence = []
	for word, tag in pos_tag(cleaned_tokens):
		if tag.startswith('NN'):
			pos = 'n'
		elif tag.startswith('VB'):
			pos = 'v'
		else:
			pos = 'a'
		lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
	return lemmatized_sentence

def remove_noise(tweet_tokens):
	stop_words = STOPWORDS
	cleaned_tokens = []

	for token, tag in pos_tag(tweet_tokens):
		token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
		token = re.sub("(@[A-Za-z0-9_]+)","", token)

		if tag.startswith("NN"):
			pos = 'n'
		elif tag.startswith('VB'):
			pos = 'v'
		else:
			pos = 'a'

		lemmatizer = WordNetLemmatizer()
		token = lemmatizer.lemmatize(token, pos)

		if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
			cleaned_tokens.append(token.lower())
	return cleaned_tokens