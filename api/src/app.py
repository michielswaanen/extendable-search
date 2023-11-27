from flask import Flask, request
from handlers.upload.upload import upload_handler
from handlers.search.search import search_handler
from handlers.index.index import index_handler
from handlers.list.videos import list_videos_handler
from handlers.list.scenes import list_scenes_handler
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

@app.route('/list/videos', methods=['GET'])
def get_videos():
    return list_videos_handler(request)

@app.route('/list/scenes/<video_id>', methods=['GET'])
def get_scenes(video_id):
    return list_scenes_handler(video_id)

if __name__ == '__main__':
    app.run(debug=True, port=3001, host="0.0.0.0")