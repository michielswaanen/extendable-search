from flask import Flask, request
from core.upload import handle_upload
from core.detect import handle_detect
from core.search import handle_search
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


@app.route('/detect', methods=['POST'])
def detect():
    # Get name from body
    name = request.json['name']
    return handle_detect('code/uploads/{}'.format(name))


@app.route('/upload', methods=['POST'])
def upload():
    return handle_upload(request)


@app.route('/search', methods=['POST'])
def search():
    return handle_search(request)


if __name__ == '__main__':
    app.run(debug=True, port=4040, host="0.0.0.0")