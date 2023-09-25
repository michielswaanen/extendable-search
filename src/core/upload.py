def handle_upload(request):
    if 'video' not in request.files:
        return 'No file uploaded', 400

    video = request.files['video']

    # Save the file to the uploads folder on the os
    video.save('uploads/{}'.format(video.filename))

    return 'File uploaded successfully'