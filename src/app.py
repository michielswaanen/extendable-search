from flask import Flask, request
from handlers.upload.upload import upload_handler
from handlers.search.search import search_handler
from handlers.index.index import index_handler
from handlers.save.save import save_handler
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/upload', methods=['POST'])
def upload():
    return upload_handler(request)

@app.route('/search', methods=['POST'])
def search():
    return search_handler(request)

@app.route('/index', methods=['POST'])
def index():
    return index_handler(request)

@app.route('/save', methods=['POST'])
def detect():
    return save_handler(request)

if __name__ == '__main__':
    app.run(debug=True, port=4040, host="0.0.0.0")