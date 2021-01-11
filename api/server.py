from flask import Flask, request
from flask_cors import CORS
import json
from jamesMain import process
from jamesClasses import inputCorpus

app = Flask(__name__)
cors = CORS(app)

@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        corpus = inputCorpus()
        for x in range(int(request.form["fileCount"])):
            file = 'file' + str(x)
            if file not in request.files:
                return 'Error with attached files'
            contents = request.files.get(file).read().decode("utf-8")
            title = request.files.get(file).filename.split(".")[0]
            corpus.addDoc(title,contents)
        results = process(corpus)
        response = json.dumps(results)
        return response, 200

if __name__ == '__main__':
    app.run(debug=True)