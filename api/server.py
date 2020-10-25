from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file1' not in request.files and 'file2' not in request.files:
            return 'No file attached in request'
        else:
            raw_data1 = request.files.get("file1").read()
            raw_data2 = request.files.get("file2").read()
            response = {
                "file1": str(raw_data1),
                "file2": str(raw_data2)
            }
            return response, 200


if __name__ == '__main__':
    app.run(debug=True)
