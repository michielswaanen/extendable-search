from core.ffmpeg.create import create_downscaled_video_copy, create_audio_copy
from core.scenes.manager import get_scene_timestamps
from modalities.visual.handler import analyze as analyze_visual
from modalities.audio.handler import analyze as analyze_audio
from modalities.faces.handler import analyze as analyze_faces
from core.ffmpeg.extract import extract_screenshot
from core.audio.audio_segment import segment_audio
from core.database.connection import save_scene_to_db, save_visual_modality_to_db, save_audio_modality_to_db, get_video, save_face_modality_to_db
import time
import av
import os
import torch
from PIL import Image

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


def create_screenshot_copies_per_scene(video, timestamps_per_scene, job_path):
    container = av.open(video)

    for scene in timestamps_per_scene:
        shots_path = f'{job_path}/scenes/{scene[0]}_{scene[-1]}/shots/'

        print("> Creating shots for scene {scene}...".format(scene=scene), flush=True)

        if not os.path.exists(shots_path):
            os.makedirs(shots_path)

        for timestamp in scene:
            screenshot = extract_screenshot(container, timestamp)

            if screenshot is not None:
                screenshot_path = f'{shots_path}{timestamp}.jpg'

                # Save nd_array to image
                image = Image.fromarray(screenshot)
                image.save(screenshot_path)


def create_audio_copy_per_scene(video_path, audio_path, timestamps_per_scene, job_path):
    container = av.open(video_path)

    for scene in timestamps_per_scene:
        try:
            audio_per_scene_path = f'{job_path}/scenes/{scene[0]}_{scene[-1]}/audio/'

            print("> Creating audio for scene {scene}...".format(scene=scene), flush=True)

            if not os.path.exists(audio_per_scene_path):
                os.makedirs(audio_per_scene_path)

            start_frame_num = scene[0]
            end_frame_num = scene[-1]

            framerate = container.streams.video[0].average_rate
            start_sec = int(start_frame_num/framerate)
            end_sec = int(end_frame_num/framerate)

            print(f"> Start: {start_sec * 1000}ms, End: {end_sec * 1000}ms", flush=True)

            # Get the start and end time of the scene
            audio = segment_audio(start_sec * 1000, end_sec * 1000, audio_path)

            # Save audio to disk
            audio.export(f'{audio_per_scene_path}audio.wav', format="wav", )
        except Exception as e:
            print(f"> Error creating audio for scene {scene}", flush=True)


def save_features_to_db(video_id, job_path, timestamps_per_scene):

    #1. Save scenes to db
    scenes = []
    scenes_path = f'{job_path}/scenes'

    for scene_timestamps in timestamps_per_scene:
        start_frame = scene_timestamps[0]
        end_frame = scene_timestamps[-1]

        scene_id = save_scene_to_db(video_id, start_frame, end_frame)

        scenes.append((scene_id, scene_timestamps))

    #2. Save visual features to db

    for scene in scenes:
        scene_id = scene[0]
        scene_timestamps = scene[1]

        embedding_path = f'{scenes_path}/{scene_timestamps[0]}_{scene_timestamps[-1]}/embeddings/'

        visual_embedding_path = f'{embedding_path}visual.pt'
        audio_embedding_path = f'{embedding_path}audio.pt'

        # Get all file paths that start with face_
        face_embedding_files = []

        for file in os.listdir(embedding_path):
            if file.startswith('face_'):
                face_embedding_files.append(file)

        # Load the embedding
        try:
            visual_embedding = torch.load(visual_embedding_path).detach().numpy().tolist()[0]
            save_visual_modality_to_db(scene_id, visual_embedding)
            print(f"> Saved visual embedding for scene {scene_id}", flush=True)
        except Exception as e:
            print(f"> Error loading visual embedding for scene {scene_id}", flush=True)

        # Save embeddings to db
        try:
            audio_embedding = torch.load(audio_embedding_path).detach().numpy().tolist()[0]
            save_audio_modality_to_db(scene_id, audio_embedding)
            print(f"> Saved audio embedding for scene {scene_id}", flush=True)
        except Exception as e:
            print(f"> Error loading audio embedding for scene {scene_id}", flush=True)

        for face_embedding_file in face_embedding_files:
            face_embedding_path = f'{embedding_path}{face_embedding_file}'
            face_embedding = torch.load(face_embedding_path)
            save_face_modality_to_db(scene_id, face_embedding)
            print(f"> Saved face embedding for scene {scene_id}", flush=True)

    pass

def index_handler(request):

    start_time = time.time()

    video_id = request.json['video_id']

    # Retrieve video from database
    video = get_video(video_id)
    job_id = video[1]


    job_path = f'code/jobs/{job_id}'

    og_video = f'{job_path}/original.mp4'
    ds_video = f'{job_path}/downscaled.mp4'
    audio = f'{job_path}/audio.mp3'

    # 1. Create workable copies of the video
    # create_downscaled_video_copy(og_video, ds_video, '480')
    create_audio_copy(og_video, audio)

    # 2. Split video into scenes
    scenes = get_scene_timestamps(og_video)

    # 3. Get timestamps of each scene, we want 8 frames per scene, evenly spaced out
    timestamps_per_scene = get_timestamps_per_scene(scenes, 8)

    # 4. Save shots to disk
    create_screenshot_copies_per_scene(og_video, timestamps_per_scene, job_path)
    create_audio_copy_per_scene(og_video, audio, timestamps_per_scene, job_path)

    # 4. Extract features from each scene

    analyze_visual(job_path, timestamps_per_scene)
    analyze_audio(job_path, timestamps_per_scene)
    analyze_faces(job_path, timestamps_per_scene)

    # 5. Save features to database
    save_features_to_db(video_id, job_path, timestamps_per_scene)

    print(f"> {len(scenes)} detected in {job_id}", flush=True)

    end_time = time.time()

    total_time = end_time - start_time
    total_minutes = int(total_time/60)
    total_seconds = round(total_time%60, 2)

    print(f"> Finished indexing {job_id} in {total_minutes}:{total_seconds} minutes", flush=True)
    return f"> Finished indexing {job_id} in {total_minutes}:{total_seconds} minutes"