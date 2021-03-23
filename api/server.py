# Library imports
import io
import pyexcel as pe
import csv
from flask import Flask, request, make_response, Response
from flask_cors import CORS
import json
import os
import sys
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Project imports
from api.jamesClasses import inputCorpus
from api.jamesConfig import cfg
from api.jamesMain import process

# Flask backend setup
app = Flask(__name__)
cors = CORS(app)

# POST request handling for uploaded files
@app.route('/upload', methods=['GET', 'POST'])
def index():
    global RESPONSE
    if request.method == 'POST':
        # Initialize an empty inputCorpus object, imported from jamesClasses
        corpus = inputCorpus()
        # Iterate through each file that should be uploaded
        for x in range(int(request.form["fileCount"])):
            # Files should be named 'file1', 'file2', 'file3', etc.
            file = 'file' + str(x)
            # If any file is not found, return an error
            if file not in request.files:
                return 'Error with attached files', 500
            # If any file is not a .txt file, return an error
            if not request.files.get(file).filename.split(".")[-1] == 'txt':
                return 'Only .txt files accepted', 500
            # Try to read and decode the contents of each file
            # If any issue is encountered, return an error
            try:
                contents = request.files.get(file).read().decode("utf-8")
            except:
                return 'Error with attached files', 500
            # If any file was empty, return an error
            if contents == "":
                return 'File empty', 500
            # For each file, read the filename without the file extension,
            #   and add these to the inputCorpus object
            title = request.files.get(file).filename.split(".")[0]
            corpus.addDoc(title, contents)
        # The number of topics is taken from the request.
        numTopics = request.form["numTopics"]
        # The process method imported from jamesMain produces results from the input corpus
        # If the number of topics was specified by the user, then the process will take in that number as an argument
        results = process(corpus) if (numTopics == "") else process(
            corpus, topicNum=int(numTopics))

        # Convert the results to a json object, and return it to the frontend
        RESPONSE = json.dumps(results)
        return RESPONSE, 200

    # If making a GET request, the page will display "No files received" until the server receives the input files
    if request.method == 'GET':
        response = RESPONSE if ("RESPONSE" in globals()
                                ) else "No files received"
        return response, 200


def create_csv_list(topics, sentiments):
    csv_list = []

    csv_list.append(["Topics"])
    for topic in [x for x in topics]:
        csv_list.append(["\n"])
        csv_list.append(["Topic Number", topic["topicnum"]])
        csv_list.append(["Coherence", topic["coherence"]])
        csv_list.append(list(topic["topicwords"][0].keys()))
        for x in topic["topicwords"]:
            csv_list.append(list(x.values()))

    csv_list.append(["\n"])
    csv_list.append(["Sentiment"])
    for sentiment in [x for x in sentiments]:
        csv_list.append(["Document Title", sentiment["doctitle"]])
        csv_list.append(list(sentiment["topics"][0].keys()))
        for x in sentiment["topics"]:
            csv_list.append(list(x.values()))

    return csv_list


@app.route('/download', methods=['GET', 'POST'])
def download():
    results = json.loads(request.form["results"])
    topic_data = results['topics']
    sentiment_data = results['sentiments']
    csv_list = create_csv_list(topic_data, sentiment_data)

    sheet = pe.Sheet(csv_list)
    i = io.StringIO()
    sheet.save_to_memory("csv", i)
    output = make_response(i.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# Backend main
if __name__ == '__main__':
    app.run(host=cfg['host']['ip'], port=cfg['host']['port'])
