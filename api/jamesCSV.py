# Library imports
import io
import pyexcel as pe
import csv

def makeCSV(results):
    '''
    Method called by server.py to convert results to a csv
    '''
    topicData = results['topics']
    sentimentData = results['sentiments']
    csvList = createCsvList(topicData, sentimentData)

    sheet = pe.Sheet(csvList)
    i = io.StringIO()
    sheet.save_to_memory("csv", i)
    return i

def createCsvList(topics, sentiments):
    csvList = []
    csvList.append(["Topics"])
    for topic in [x for x in topics]:
        csvList.append(["\n"])
        csvList.append(["Topic Number", topic["topicnum"]])
        csvList.append(["Coherence", topic["coherence"]])
        csvList.append(list(topic["topicwords"][0].keys()))
        for y in topic["topicwords"]:
            csvList.append(list(y.values()))
        csvList.append(list(topic["examplesentences"][0].keys()))
        for y in topic["examplesentences"]:
            csvList.append(list(y.values()))
    csvList.append(["\n"])
    csvList.append(["Sentiment"])
    for sentiment in [x for x in sentiments]:
        csvList.append(["Document Title", sentiment["doctitle"]])
        csvList.append(list(sentiment["topics"][0].keys()))
        for y in sentiment["topics"]:
            csvList.append(list(y.values()))

    return csvList