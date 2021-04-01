# Library imports
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
from api.jamesCSV import makeCSV
from api.jamesMain import process
from api.jamesPreProcessing import separateSentences

# Flask backend setup
app = Flask(__name__)
cors = CORS(app)

# POST request handling for uploaded files
@app.route('/upload', methods=['GET', 'POST'])
def index():
    # Try to process uploaded files
    try:
        if request.method == 'POST':
            # Initialize an empty inputCorpus object, imported from jamesClasses
            corpus = inputCorpus()
            # Initialize sentence count
            sentenceCount = 0
            # Iterate through each file that should be uploaded
            for x in range(int(request.form["fileCount"])):
                # Files should be named 'file1', 'file2', 'file3', etc.
                file = 'file' + str(x)
                # If any file is not found, return an error
                if file not in request.files:
                    return 'Error with attached file(s)', 500
                # If any file is not a .txt file, return an error
                if not request.files.get(file).filename.split(".")[-1] == 'txt':
                    return 'Only .txt files accepted', 500
                # Try to read and decode the contents of each file
                # If any issue is encountered, return an error
                try:
                    contents = request.files.get(file).read().decode("utf-8")
                except:
                    return 'Error with attached file(s)', 500
                # If any file was empty, return an error
                if contents == "":
                    return 'File empty', 500
                # For each file, read the filename without the file extension,
                #   and add these to the inputCorpus object
                title = request.files.get(file).filename.split(".")[0]
                corpus.addDoc(title, contents)
                # Add the sentence count to the running total
                sentenceCount += len(separateSentences(contents))
            # The number of topics is taken from the request
            try:
                numTopics = int(request.form["numTopics"])
            except:
                return "Error with number of topics", 500
            # The topic number cannot be higher than the topic max
            if numTopics > cfg['topicmax']:
                return "Topic number greater than topic max " + str(cfg['topicmax']), 500
            # The topic number cannot be higher than the total number of sentences
            if numTopics > sentenceCount:
                return "Topic number greater than sentence count", 500
            # The dataset selected for sentiment analysis is taken from the request
            try:
                datasetChoice = request.form["datasetChoice"]
            except:
                return 'Error with selected dataset', 500
            # The process method imported from jamesMain produces results from the input corpus
            results = process(corpus, numTopics, datasetChoice)
            if results == None:
                return 'Error with attached file(s)', 500
            # Convert the results to a json object, and return it to the frontend
            response = json.dumps(results)
            return response, 200

        # If making a GET request, the page will display "No files received"
        if request.method == 'GET':
            return "No files received", 200
    # If processing files fails, return error result
    except Exception as e:
        return "Error processing attached files: " + str(e), 500

# POST request handling for downloading results
@app.route('/download', methods=['POST'])
def download():
    # Try to download csv of given results
    try:
        # Load the results and hidden topics from the request json object
        results = json.loads(request.form["results"])
        hidden = json.loads(request.form["hiddenTopics"])
        # If the user has hidden all topics, return an error
        if len(hidden) >= len(results["topics"]):
            return "All topics hidden", 500
        # Construct the csv
        data = makeCSV(results,hidden)
        # Construct the response
        output = make_response(data)
        output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        output.headers["Content-type"] = "text/csv"
        # Return the response
        return output
    # If csv generation fails, return error result
    except:
        return "Error downloading results", 500

# Backend main
if __name__ == '__main__':
    app.run(host=cfg['host']['ip'], port=cfg['host']['port'], threaded=True)
