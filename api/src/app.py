from flask import Flask, request
from handlers.upload.upload import upload_handler
from handlers.search.search import search_handler
from handlers.index.index import index_handler
from handlers.list.videos import list_videos_handler
from handlers.list.video import list_video_handler
from handlers.list.scenes import list_scenes_handler
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, origins='*', allow_headers='*')
load_dotenv()

@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    return upload_handler(request)

@app.route('/search', methods=['POST'])
@cross_origin()
def search():
    return search_handler(request)

@app.route('/index', methods=['POST'])
@cross_origin()
def index():
    return index_handler(request)

@app.route('/videos/<video_id>/scenes', methods=['GET'])
@cross_origin()
def get_scenes(video_id):
    return list_scenes_handler(video_id)

@app.route('/videos/<video_id>', methods=['GET'])
@cross_origin()
def get_video(video_id):
    return list_video_handler(video_id)

@app.route('/videos', methods=['GET'])
@cross_origin()
def get_videos():
    return list_videos_handler(request)

if __name__ == '__main__':
    app.run(debug=True, port=3001, host="0.0.0.0")