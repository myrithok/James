from flask import Flask, request
from flask_cors import CORS
from jamesMain import process
from jamesClasses import jamesCorpus

app = Flask(__name__)
cors = CORS(app)

@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file attached in request'
        else:
            corpus = inputCorpus()
            corpus.addDoc(request.files.get("file").read())
            corpus.addDoc(request.files.get("file").read())
            results = process(corpus)
            response = {
                "results": results
            }
            return response, 200

if __name__ == '__main__':
    app.run(debug=True)