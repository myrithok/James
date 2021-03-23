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
            # The number of topics is taken from the request.
            numTopics = request.form["numTopics"]
            # The process method imported from jamesMain produces results from the input corpus
            # If the number of topics was specified by the user, then the process will take in that number as an argument
            results = process(corpus) if (numTopics == "") else process(
                corpus, topicNum=int(numTopics))
            if results == None:
                return 'Error with attached file(s)', 500
            # Convert the results to a json object, and return it to the frontend
            response = json.dumps(results)
            return response, 200

        # If making a GET request, the page will display "No files received"
        if request.method == 'GET':
            return "No files received", 200
    # If processing files fails, return error result
    except:
        return "Error processing attached files", 500

# POST request handling for downloading results
@app.route('/download', methods=['POST'])
def download():
    # Try to download csv of given results
    try:
        # Load the results from the request json object
        results = json.loads(request.form["results"])
        # Construct the csv
        data = makeCSV(results)
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
    app.run(host=cfg['host']['ip'], port=cfg['host']['port'])
