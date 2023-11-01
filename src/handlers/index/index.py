from core.ffmpeg.create import create_downscaled_video_copy, create_audio_copy
from core.scenes.manager import get_scene_timestamps
from core.opencv.fps import get_fps
from modalities.visual.handler import analyze as analyze_visual
import time
# scenes: [(0, 0, 110), (1, 110, 299), (1, 299, 488), (1, 488, 678), (1, 678, 867), (1, 867, 1056), (1, 1056, 1245), (1, 1245, 1434), (1, 1434, 1623), (1, 1623, 1812), (1, 1812, 2002), (1, 2002, 2191), (1, 2191, 2380), (1, 2380, 2569), (1, 2569, 2758), (1, 2758, 2948), (1, 2948, 3137), (1, 3137, 3326), (1, 3326, 3515), (1, 3515, 3704), (1, 3704, 3893), (1, 3893, 4082), (1, 4082, 4272), (1, 4272, 4461), (1, 4461, 4650), (1, 4650, 4839), (1, 4839, 5028), (1, 5028, 5218), (1, 5218, 5407), (1, 5407, 5596), (1, 5596, 5785), (2, 5785, 5876)]
# Where the first number is the scene index, the second number is the start frame and the third number is the end frame
def print_scenes(scenes, fps):
    # Print the scene index and the start and end frame of each scene
    # Start and end time should be in the minutes:seconds format
    # Scene index should be displayed as 1.1, 2.3 (depending on the scene index)
    head_scene_index = scenes[0][0]
    sub_scene_index = 0

    for scene_idx in range(len(scenes)):

        if scenes[scene_idx][0] == head_scene_index:
            sub_scene_index += 1
        else:
            sub_scene_index = 0
            head_scene_index = scenes[scene_idx][0]

        start_time = round(scenes[scene_idx][1]/fps, 2)
        end_time = round(scenes[scene_idx][2]/fps, 2)

        start_minutes = int(start_time/60)
        start_seconds = round(start_time%60, 2)

        end_minutes = int(end_time/60)
        end_seconds = round(end_time%60, 2)

        index = f'{scenes[scene_idx][0]}.{sub_scene_index}'

        print(f'Scene {index}: {start_minutes}:{start_seconds} - {end_minutes}:{end_seconds}', flush=True)


def get_timestamps_per_scene(scenes, per_scene=8):
    timestamps_per_scene = []

    for scene in scenes:
        scene_length = scene[2] - scene[1]
        every_n = round(scene_length/per_scene)
        local_samples = [(every_n * n) + scene[1] for n in range(8)]
        timestamps_per_scene.append(local_samples)

    return timestamps_per_scene

def index_handler(request):

    start_time = time.time()

    job_id = request.json['job_id']
    job_path = f'code/jobs/tmp/{job_id}'

    og_video = f'{job_path}/original.mp4'
    ds_video = f'{job_path}/downscaled.mp4'
    audio = f'{job_path}/audio.mp3'

    # 1. Create workable copies of the video
    create_downscaled_video_copy(og_video, ds_video, '480')
    create_audio_copy(og_video, audio)

    # 2. Split video into scenes
    scenes = get_scene_timestamps(ds_video)

    # Get timestamps of each scene, we want 8 frames per scene, evenly spaced out
    timestamps_per_scene = get_timestamps_per_scene(scenes, 8)

    # fps = get_fps(ds_video)

    # 3. Print out found scenes and their timestamps
    # print_scenes(scenes, fps)

    # 4. Extract features from each scene

    analyze_visual(job_path, timestamps_per_scene)

    print(f"> {len(scenes)} detected in {job_id}", flush=True)

    end_time = time.time()

    total_time = end_time - start_time
    total_minutes = int(total_time/60)
    total_seconds = round(total_time%60, 2)

    print(f"> Finished indexing {job_id} in {total_minutes}:{total_seconds} minutes", flush=True)
    return f"> Finished indexing {job_id} in {total_minutes}:{total_seconds} minutes"