import os
import scenedetect as sd

def handle_detect(video_path):

    video = sd.open_video(video_path)

    sm = sd.SceneManager()

    sm.add_detector(sd.ContentDetector(threshold=27.0))
    sm.detect_scenes(video)

    scenes = sm.get_scene_list()

    print(scenes, flush=True)

    return 'OK'