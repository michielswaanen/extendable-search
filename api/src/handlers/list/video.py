from core.database.connection import get_video

def list_video_handler(video_id):

    if not video_id:
        return 'Missing video_id', 400

    # Get all videos from db
    video = get_video(video_id);

    return video