from core.jobs.save import save_job_on_disk

def upload_handler(request):

    if 'video' not in request.files:
        return 'No file uploaded', 400

    video = request.files['video']

    # Save the video to a randomly generated folder
    video_path = save_job_on_disk(video)

    return video_path