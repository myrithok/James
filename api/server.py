# Library imports
from flask import Flask, request
from flask_cors import CORS
import json
import os
import sys
# Add James to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Project imports
from api.jamesClasses import inputCorpus
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
                return 'Error with attached files'
            # For each file, read and decode the contents,
            #   check that the file is not empty,
            #   read the filename without the file extension, 
            #   and add these to the inputCorpus object
            contents = request.files.get(file).read().decode("utf-8")
            if contents = "":
                return 'Attached file empty'
            title = request.files.get(file).filename.split(".")[0]
            corpus.addDoc(title, contents)
        # The number of topics is taken from the request.
        numTopics = request.form["numTopics"]
        # The process method imported from jamesMain produces results from the input corpus
        # If the number of topics was specified by the user, then the process will take in that number as an argument
        results = process(corpus) if (numTopics == "") else process(corpus, topicNum=int(numTopics))

        # Convert the results to a json object, and return it to the frontend
        RESPONSE = json.dumps(results)
        return RESPONSE, 200

    # If making a GET request, the page will display "No files received" until the server receives the input files
    if request.method == 'GET':
        response = RESPONSE if ("RESPONSE" in globals()) else "No files received"
        return response, 200

# Backend main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
