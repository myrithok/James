from tensorflow import keras
import pandas as pd
import re
from keras.utils.np_utils import to_categorical
from sklearn.model_selection import train_test_split
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
# from sklearn.feature_extraction.text import TfidfTransformer


def read_file(filename, filetype):
    if filetype == "txt":
        with open(filename, "r") as f:
            data = f.read()
            data = data.split("\n")

        for line in range(len(data)):
            data[line] = data[line].split("\t")

        return pd.DataFrame(data, columns=['text', 'sentiment'])
    elif filetype == "csv":
        return pd.read_csv(filename)
    else:
        raise Exception("Invalid filetype")


def preprocess_data(data):
    # Preprocessing
    # Set to lowercase
    data['text'] = data['text'].apply(lambda x: x.lower())

    # remove special characters
    data['text'] = data['text'].apply(
        (lambda x: re.sub('[^a-zA-z0-9\s]', '', x)))
    return data


def get_tokenizer(data, features):

    # define 2000 max features
    # use tokenizer to vectorize and convert text into seuqnces

    # the max number of words to keep, based on word frequency
    # features

    # creates a dictionary based on the word frequency

    tokenizer = Tokenizer(num_words=features, split=' ')

    # creates a dictionary based on the word frequency. Each word gets a unique integer value
    # lower integer means more frequent words
    tokenizer.fit_on_texts(data['text'].values)
    return tokenizer

# Trains a model. Only needs to be run once to initiate model


def train_RNN(data, features, name):
    # read files
    data = preprocess_data(data)
    tokenizer = get_tokenizer(data, features)

    # transforms each text in texts to a sequence of integers
    X = tokenizer.texts_to_sequences(data['text'].values)

    # ensures all seuqnces in a list have the same length by padding 0s in the beginning and end of each
    X = pad_sequences(X)

    # create LSTM network
    # embed_dim, lstm_out, batch_size and dropout_x are hyperparameters
    # ie they need to be tweaked manually
    embed_dim = 128
    lstm_out = 196

    # initialize model
    model = Sequential()

    # Embedding layer
    # first argument: number of distinct words in the training set
    # second arg: size of embedding vectors
    # input length: size of each input sequence
    model.add(Embedding(features, embed_dim, input_length=X.shape[1]))

    # Dropout layer
    # arg: rate = fraction of the input units to drop
    # it is the probability of setting each input to the layer to zero
    # added to a model between existing layers
    # helps prevent overfitting. regularization method
    model.add(SpatialDropout1D(0.4))

    # LSTM Recurrent NN layer
    # arg1: dimensionality of the output space
    # dropout: fraction of the units to drop for the linear transformation of the inputs
    # recurrent dropout: Fraction of the units to drop for the linear transformation of the recurrent state.
    model.add(LSTM(lstm_out, dropout=0.2, recurrent_dropout=0.2))

    # Dense layer
    # regular deeply connected neural network layer
    # performs activation(dot(input, kernel) + bias)
    # use softmax as activation because network is using categorical
    # crossentropy and softmax is right for that
    # arg 1 : number of units which will determine the output shape
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])
    # print(model.summary())

    # converts categorical variable into indicator variables
    # a matrix where the columns are characters and the rows are indexes
    Y = pd.get_dummies(data['sentiment']).values

    # split training and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.33, random_state=42)
    # print(X_train.shape,Y_train.shape)
    # print(X_test.shape,Y_test.shape)

    # number of samples that will be propagated through the network
    batch_size = 32
    # verbose has to do with the information displayed when training the model. 0 for no output
    model.fit(X_train, Y_train, epochs=7, batch_size=batch_size, verbose=2)
    model.save("api//model//" + name)
    #validation_size = 500
    #X_validate = X_test[-validation_size:]
    #Y_validate = Y_test[-validation_size:]
    #X_test = X_test[:-validation_size]
    #Y_test = Y_test[:-validation_size]

    # the lower the loss, the better the model
    # accuracy: number of misclassified
    print("Evaluating model")
    print(X_test.shape)
    print(Y_test.shape)
    loss, acc = model.evaluate(
        X_test, Y_test, verbose=2, batch_size=batch_size)
    print("loss: %.2f" % (loss))
    print("acc: %.2f" % (acc))


# trainRNN()

def load_RNN(name):
    model = keras.models.load_model('api//model//' + name)
    return model


def RNN_prediction(model, documents, tokenizer, datashape):
    # vectorizing the tweet by the pre-fitted tokenizer instance
    documents = tokenizer.texts_to_sequences(documents)
    # padding the tweet to have exactly the same shape as `embedding_2` input
    # datashape = 55 for SA, 91 for SO
    documents = pad_sequences(documents, maxlen=datashape, dtype='int32', value=0)
    sentiment = model.predict(documents, batch_size=32)
    return sentiment


# dataset from : https://www.kaggle.com/marklvl/sentiment-labelled-sentences-data-set
def reTrainSA():
    data = read_file("trainingdata//amazon_cells_labelled.txt","txt") + \
        read_file("trainingdata//imdb_labelled.txt","txt") + \
        read_file("trainingdata//yelp_labelled.txt","txt")
    train_RNN(data, 2000, "SAmodel")

def getPredictor(model_name, files, filetype, features):
    # read files for tokenizer
    data = pd.concat([read_file(file, filetype) for file in files])

    data = preprocess_data(data)
    # create tokenizer
    tokenizer = get_tokenizer(data, features)

    model = load_RNN(model_name)
    return model, tokenizer
