
import os
import sys
import pandas as pd
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api.jamesRNNSA import preprocess_data, get_tokenizer, train_RNN, read_file, RNN_prediction, getPredictor
import api.jamesRNNSA

def read_folder(path, trainfolder, testfolder):
    train = [path+trainfolder+file for file in os.listdir(path+trainfolder)]
    test = [path+testfolder+file for file in os.listdir(path+testfolder)]
    return train, test


def createDataSet(files):
    X = []
    for file in files:
        with open(file, encoding="utf8") as f:
            data = f.read()
            label = 1 if file[-5] == "Y" else 0
            X.append([data[:500], label])  # takes a max of 500 characters

    return X

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
    comb.to_csv("api//trainingdata//convote_v1.1//SO_congressional_data.csv", index=False)

def reTrainSO():
    data = read_file("api//trainingdata//convote_v1.1//SO_congressional_data.csv","csv")
#tokenizer = get_tokenizer(train_data, 500)
    train_RNN(data, 500, "SOmodel")

file = "api//trainingdata//convote_v1.1//SO_congressional_data.csv"
ftype = "csv"
features = 500
model, tk = getPredictor("SOmodel//", [file], ftype, features)

docs = ["i disagree with this","i oppose this","this makes sense i agree with it"]
ret = RNN_prediction(model,  docs, tk, 91)
print(ret)
