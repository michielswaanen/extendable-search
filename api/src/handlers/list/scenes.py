from core.database.connection import get_scenes

def list_scenes_handler(video_id):

    if not video_id:
        return 'Missing video_id', 400

    # Get all scenes from db
    scenes = get_scenes(video_id);

    return scenes