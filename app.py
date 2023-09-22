from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():

    if 'video' not in request.files:
        return 'No file uploaded', 400

    video = request.files['video']

    # Save the file to the uploads folder on the os
    video.save('uploads/{}'.format(video.filename))


    return 'File uploaded successfully'

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # Do something with the search query
    return 'Search results for "{}"'.format(query)

@app.route('/', methods=['GET'])
def index():
    return 'Hello World!!!'

if __name__ == '__main__':
    app.run(debug=True, port=4040, host="0.0.0.0")