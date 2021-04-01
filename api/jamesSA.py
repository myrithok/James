# Library imports
import os
import sys
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
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Project imports
from api.jamesConfig import cfg
# from sklearn.feature_extraction.text import TfidfTransformer

# SO Generate csv dataset
'''
Helper function to generate the dataset for the support-oppose analysis

Parameters
----------
        path: string
                the path to the training and test folders

        trainfolder: string
                the name of the train folder containing the training data
        
        testfolder: string
                the name of the test folder containing the testing data

Output
------
        train, test
                train and test are lists containing the path to each file in the training and test set respectively
'''
def read_folder(path, trainfolder, testfolder):
    train = [path+trainfolder+file for file in os.listdir(path+trainfolder)]
    test = [path+testfolder+file for file in os.listdir(path+testfolder)]
    return train, test

'''
Extract the text information and labels from the congressional dataset

Parameters
----------
        files: list
             a list of file names with their path    

Output
------
        file_data: list
                a list of tuples where each tuple contains the file text and the sentiment label.


'''
def createDataSet(files):
    file_data = []
    for file in files:
        with open(file, encoding="utf8") as f:
            data = f.read()
            label = 1 if file[-5] == "Y" else 0 # sentiment label is contained in the name of the text file in the format: ___X.txt where X is the label
            file_data.append([data[:500], label])  # takes a max of 500 characters

    return file_data

'''
Generate the csv dataset for the support-oppose analysis from the textfiles in the original source

Output
------
        void
            saves a csv file to the trainingdata folder


'''
def generateSOdata():
    path = "api\\trainingdata\\convote_v1.1\\data_stage_three\\"
    trainfolder = "training_set\\"
    testfolder = "test_set\\"

    tr, te = read_folder(path, trainfolder, testfolder)

    train = createDataSet(tr)
    test = createDataSet(te)

    train_data = preprocess_data(train)
    test_data = preprocess_data(test)

    comb = pd.concat([train_data,test_data])
    comb.to_csv(cfg[path]["so"][1][0], index=False)




# SO + SA read file
'''
Reads a dataset file for use in training the sentiment model and tokenizer

Parameters
----------
        filename: string
             the name of the dataset file   
        filetype: string
             the filetype of the dataset file. Only txt and csv are acceptable

Output
------
        pd.DataFrame
                a pandas dataframe where each row contains a data point and there are two columns for the data point text and sentiment label.


'''
def read_file(filename, filetype):
    # text file
    if filetype == "txt":
        with open(filename, "r") as f:
            data = f.read()
            data = data.split("\n")

        for line in range(len(data)):
            data[line] = data[line].split("\t")

        return pd.DataFrame(data, columns=['text', 'sentiment'])
    # csv file
    elif filetype == "csv":
        return pd.read_csv(filename)
    else:
        raise Exception("Invalid filetype")

'''
Preprocesses text data for sentiment analysis. Removes non letters and numbers and converts all words to lowercase.

Parameters
----------
        data: pd.DataFrame
             a pandas dataframe with a column named "text" that contains the text data of each data point


Output
------
        data: pd.DataFrame
                a pandas dataframe where each row contains a data point and there are two columns for the data point text and sentiment label.


'''
def preprocess_data(data):
    # Preprocessing
    # Set to lowercase
    data['text'] = data['text'].apply(lambda x: x.lower())

    # remove special characters
    data['text'] = data['text'].apply(
        (lambda x: re.sub('[^a-zA-z0-9\s]', '', x)))
    return data

'''
Trains the tokenizer for use in training the sentiment models and for making predictions.

Parameters
----------
        data: pd.DataFrame
             a pandas dataframe with a column named "text" that contains the text data of each data point and a column "sentiment" which contains the corresponding sentiment label.

        features: Int
            the maximum number of words to keep, based on word frequency


Output
------
        tokenizer: tf.keras.preprocessing.text.Tokenizer
                a trained tokenizer which allows us to vectorize a piece of text


'''
def get_tokenizer(data, features):
    # use tokenizer to vectorize and convert text into seuqnces
    tokenizer = Tokenizer(num_words=features, split=' ')
    # creates a dictionary based on the word frequency. Each word gets a unique integer value
    # lower integer means more frequent words
    tokenizer.fit_on_texts(data['text'].values)
    return tokenizer


'''
Trains an RNN model. Only needs to be run once to initiate model. Used as a helper in reTrainModel.
Parameters here may be changed if the developer would like to try a different RNN architecture 

Parameters
----------
        data: pd.DataFrame
             a pandas dataframe with a column named "text" that contains the text data of each data point and a column "sentiment" which contains the corresponding sentiment label.

        features: Int
            the maximum number of words to keep, based on word frequency
        
        name: String
            the name of the seniment analysis model. The name will determine the save location and model name for future referencing.


Output
------
        void
                saves a sentiment model in the api/model folder and outputs the training accuracy and loss


'''
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

    # the lower the loss, the better the model
    # accuracy: number of misclassified
    print("Evaluating model")
    print(X_test.shape)
    print(Y_test.shape)
    loss, acc = model.evaluate(
        X_test, Y_test, verbose=2, batch_size=batch_size)
    print("loss: %.2f" % (loss))
    print("acc: %.2f" % (acc))


'''
Loads an RNN model

Parameters
----------
        name: string
             The name of the RNN model


Output
------
        model: tf.keras.Model
                a tensorflow model object which can be used for predictions


'''
def load_RNN(name):
    model = keras.models.load_model(name)
    return model


'''
Wrapper for RNN_prediction to return values in the expected format

Parameters
----------
        model: tf.keras.Model
            RNN sentiment model
        documents: list
            a list containing a single string which is the text to be analyzed
        tokenizer: tf.keras.preprocessing.text.Tokenizer
            tokenizer that was trained on the same data as the RNN model
        datashape:
            the shape of the data after the model was trained. For the current model, datashape = 55 for SA, 91 for SO

Output
------
        float
                a sentiment score between 0 and 1 which represents the probability that the text is positive (if SAmodel) or in support (if SOmodel)


'''
def getSentenceSentiment(model, documents, tokenizer, datashape):
    results = RNN_prediction(model, documents, tokenizer, datashape)
    return float(results[0][1])

'''
Method to make sentiment predictions given a trained model

Parameters
----------
        model: tf.keras.Model
            RNN sentiment model
        documents: list
            a list containing a single string which is the text to be analyzed
        tokenizer: tf.keras.preprocessing.text.Tokenizer
            tokenizer that was trained on the same data as the RNN model
        datashape:
            the shape of the data after the model was trained. For the current model, datashape = 55 for SA, 91 for SO

Output
------
        list
                a list with 2 sentiment scores where the first value is the negative/opposition probability 
                and the 2nd value is the positive/support probability

'''
def RNN_prediction(model, documents, tokenizer, datashape):
    # vectorizing the tweet by the pre-fitted tokenizer instance
    documents = tokenizer.texts_to_sequences(documents)
    # padding the tweet to have exactly the same shape as `embedding_2` input
    # datashape = 55 for SA, 91 for SO
    documents = pad_sequences(documents, maxlen=datashape, dtype='int32', value=0)
    sentiment = model.predict(documents, batch_size=32)
    return sentiment


'''
Trains an RNN model. Only needs to be run once to initiate model.


Parameters
----------
        modelType: string
             (see Config File) sets the model parameters to specify which sentiment model to train

        features: Int
            the maximum number of words to keep, based on word frequency. Used in the tokenizer and when training the model
        
        modelName: String
            the name of the seniment analysis model. The name will determine the save location and model name for future referencing.
            The name should be either SAmodel or SOmodel


Output
------
        void
                saves a sentiment model in the api/model folder and outputs the training accuracy and loss


'''
def reTrainModel(modelType, features, modelName):
    data = pd.DataFrame(columns=['text', 'sentiment'])
    # modeltype is "pn" for positive negative sentiment and "so" for support oppose
    fileinfo = cfg['path'][modelType]
    files = fileinfo[1]
    filetype = fileinfo[2]
    fileDataFrames = []
    for file in files:
        fileDataFrames.append(read_file(file,filetype))
    data = data.append(fileDataFrames)
    train_RNN(data, features, modelName)

'''
Gets a trained model and tokenizer for use in making predictions


Parameters
----------
        model_name: String
             the name of the model to be loaded

        files: list
            a list of files containing the training data
        
        filetype: String
            the type of files given in files (either csv or txt)
        
        features: Int
            the maximum number of words to keep, based on word frequency. Used in the tokenizer and when training the model

Output
------
        model, tokenizer
                returns a trained tensorflow model object and a trained tokenizer object


'''
def getPredictor(model_name, files, filetype, features):
    # read files for tokenizer
    data = pd.concat([read_file(file, filetype) for file in files])

    data = preprocess_data(data)
    # create tokenizer
    tokenizer = get_tokenizer(data, features)

    model = load_RNN(model_name)
    return model, tokenizer
