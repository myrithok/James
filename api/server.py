from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/upload', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        for x in range(int(request.form["fileCount"])):
            if 'file' + str(x) not in request.files:
                return 'Error with attached files'
        # This is just dummy code
        # This will also need to be a loop like above
        raw_data = request.files.get("file0").read()
        response = {
            "file0": str(raw_data)}
        return response, 200


if __name__ == '__main__':
    app.run(debug=True)
