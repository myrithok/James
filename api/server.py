#Library imports
from flask import Flask, request
from flask_cors import CORS
import json
#Project imports
from jamesMain import process
from jamesClasses import inputCorpus

#Flask backend setup
app = Flask(__name__)
cors = CORS(app)

#POST request handling for uploaded files
@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #Initialize an empty inputCorpus object, imported from jamesClasses
        corpus = inputCorpus()
        #Iterate through each file that should be uploaded
        for x in range(int(request.form["fileCount"])):
            #Files should be named 'file1', 'file2', 'file3', etc.
            file = 'file' + str(x)
            #If any file is not found, return an error
            if file not in request.files:
                return 'Error with attached files'
            #For each file, read and decode the contents, 
            #   read the filename without the file extension, 
            #   and add these to the inputCorpus object
            contents = request.files.get(file).read().decode("utf-8")
            title = request.files.get(file).filename.split(".")[0]
            corpus.addDoc(title,contents)
        #The process method imported from jamesMain produces results from the input corpus
        results = process(corpus)
        #Convert the results to a json object, and return it to the frontend
        response = json.dumps(results)
        return response, 200

#Backend main
if __name__ == '__main__':
    app.run(debug=True)