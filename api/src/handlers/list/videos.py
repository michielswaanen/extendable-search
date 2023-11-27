from core.database.connection import get_videos

def list_videos_handler(request):

    # Get all videos from db
    videos = get_videos();

    return videos