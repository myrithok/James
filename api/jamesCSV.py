# Library imports
import io
import pyexcel as pe
import csv

def makeCSV(results):
    '''
    Method called by server.py to convert a result set into a csv

    Parameters
    ----------
            results: json
                    a result set from running james as a
                    json object

    Output
    ------
            str
                    the contents of the csv as a string
    '''
    # Create a 2-dimensional list from the result set using
    #   createCsvList, found below
    csvList = createCsvList(results)
    # Convert the csv list into a csv
    sheet = pe.Sheet(csvList)
    i = io.StringIO()
    sheet.save_to_memory("csv", i)
    # Load the contents of the csv as a string, and return it
    output = i.getvalue()
    return output

def createCsvList(results):
    '''
    Method called by makeCSV, above, to convert a result set
    into a 2-dimensional list that can be inserted  into a csv

    Parameters
    ----------
            results: json
                    a result set from running james as a
                    json object

    Output
    ------
            list:
                    a 2-dimensional list, which each element of
                    the outer list represents a row of the final csv,
                    and each element of each inner list represents a
                    cell in that row
    '''
    # Initialize the outer list
    csvList = []
    # Add the title for the topic section
    csvList.append(["Topics"])
    # Iterate through each topic
    for topic in [x for x in results['topics']]:
        # Insert the topic number and coherence score
        csvList.append(["\n"])
        csvList.append(["Topic Number", topic["topicnum"]])
        csvList.append(["Coherence", topic["coherence"]])
        # Insert the topic word
        csvList.append(list(topic["topicwords"][0].keys()))
        for y in topic["topicwords"]:
            csvList.append(list(y.values()))
        # Insert the example sentences
        csvList.append(list(topic["examplesentences"][0].keys()))
        for y in topic["examplesentences"]:
            csvList.append(list(y.values()))
    # Add the title for the sentiment section
    csvList.append(["\n"])
    csvList.append(["Sentiment"])
    # Iterate through each document
    for sentiment in [x for x in results['sentiments']]:
        # Insert the document title
        csvList.append(["Document Title", sentiment["doctitle"]])
        # Insert the document topic weights and sentiments
        csvList.append(list(sentiment["topics"][0].keys()))
        for y in sentiment["topics"]:
            csvList.append(list(y.values()))
    # Return the final list
    return csvList