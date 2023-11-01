import scenedetect as sd

def get_scene_timestamps(video_path):
    """
    This function detects scenes in a video and returns a list of frame samples
    for each scene. Every scene exists of 8 frame samples, evenly distributed across the scene.

    """
    print(f'> Detecting scenes in {video_path}...', flush=True)

    video = sd.open_video(video_path)

    sm = sd.SceneManager()

    sm.add_detector(sd.ContentDetector(threshold=37.0))
    sm.detect_scenes(video)

    scenes = sm.get_scene_list()

    max_duration_per_scene = 8 # seconds
    scenes_under_max_length = []

    # Check if there are any scenes that are longer then 8 seconds
    # If so, split them up into multiple scenes
    for scene_idx in range(len(scenes)):
        frames_in_scenes = abs(scenes[scene_idx][0].frame_num - scenes[scene_idx][1].frame_num)
        scene_duration_in_seconds = frames_in_scenes / video.frame_rate

        if scene_duration_in_seconds >= max_duration_per_scene:
            splits = round(scene_duration_in_seconds / max_duration_per_scene)
            seconds_per_split = scene_duration_in_seconds / splits

            def calc_addition(n):
                return (n * seconds_per_split * video.frame_rate)

            for n in range(splits):
                starts_at = scenes[scene_idx][0].frame_num

                start_frame = round(starts_at + calc_addition(n))
                end_frame = round(starts_at + calc_addition(n+1))
                scenes_under_max_length.append((scene_idx, start_frame, end_frame))
        else:
            scenes_under_max_length.append((scene_idx, scenes[scene_idx][0].frame_num, scenes[scene_idx][1].frame_num))

    return scenes_under_max_length