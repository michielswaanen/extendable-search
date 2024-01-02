from core.jobs.save import save_job_on_disk
from core.database.connection import save_video_to_db, init_tables
from core.opencv.metadata import get_fps, get_duration

def upload_handler(request):

    init_tables()

    print(request.files, flush=True)

    if 'video' not in request.files:
        return 'No file uploaded', 400

    video = request.files['video']

    # Save the video to a randomly generated folder
    job_id, video_path = save_job_on_disk(video)

    # Get fps
    fps = get_fps(video_path)
    duration = get_duration(video_path)

    video_id = save_video_to_db(job_id, video.name, fps, duration)

    return {
        'video_id': video_id
    }