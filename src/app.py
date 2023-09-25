from flask import Flask, request, Response
from core.upload import handle_upload
from core.detect import handle_detect

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    # Get name from body
    name = request.json['name']
    return handle_detect('uploads/{}'.format(name))


@app.route('/upload', methods=['POST'])
def upload():
    return handle_upload(request)


@app.route('/search', methods=['POST'])
def search():
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, port=4040, host="0.0.0.0")