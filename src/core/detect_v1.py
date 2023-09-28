import os
import scenedetect as sd
import cv2
from PIL import Image
from transformers import CLIPProcessor
from core.database import Database
from core.embed import embed, average_embedding, save_tensor, load_tensor, normalize_embedding


def handle_detect_v1(video_path):

    ##############################
    #        Detect scenes       #
    ##############################

    video = sd.open_video(video_path)

    sm = sd.SceneManager()

    sm.add_detector(sd.ContentDetector(threshold=27.0))
    sm.detect_scenes(video)

    scenes = sm.get_scene_list()

    print(scenes, flush=True)

    ##############################
    #     Calculate samples      #
    ##############################

    cap = cv2.VideoCapture(video_path)

    every_n = 2 # number of samples per scene
    no_of_samples = 10 # number of samples per scene

    scenes_frame_samples = []

    for scene_idx in range(len(scenes)):
        scene_length = abs(scenes[scene_idx][0].frame_num - scenes[scene_idx][1].frame_num)
        every_n = round(scene_length/no_of_samples)
        local_samples = [(every_n * n) + scenes[scene_idx][0].frame_num for n in range(no_of_samples)]

        scenes_frame_samples.append(local_samples)

    print(scenes_frame_samples, flush=True)

    ##############################
    #         Embedding          #
    ##############################

    scene_clip_embeddings = [] # to hold the scene embeddings in the next step

    # Get frames in video
    frames = sd.get_video_frames(video_path, scenes)

    for scene_idx in range(len(scenes_frame_samples)):
        scene_samples = scenes_frame_samples[scene_idx]

        pixel_tensors = [] # holds all of the clip embeddings for each of the samples

        for frame_sample in scene_samples:
            cap.set(1, frame_sample)
            ret, frame = cap.read()
            if not ret:
                print('failed to read', ret, frame_sample, scene_idx, frame)
                break

            pil_image = Image.fromarray(frame)

            print('Calculating embedding #', frame_sample, flush=True)

            clip_pixel_values = embed(pil_image)

            pixel_tensors.append(clip_pixel_values)

        avg_tensor = average_embedding(pixel_tensors)
        scene_clip_embeddings.append(save_tensor(normalize_embedding(avg_tensor)))

    ##############################
    #          Database          #
    ##############################

    print('Saving to database', flush=True)

    # Init database
    database = Database(
        uri=os.getenv('DATABASE_URI')
    )

    print('Connecting to database', flush=True)

    # Connect to database
    database.connect()

    # Create vector extension
    database.query("CREATE EXTENSION IF NOT EXISTS embedding")
    database.query("CREATE TABLE IF NOT EXISTS videos (id SERIAL PRIMARY KEY, path VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    database.query("CREATE TABLE IF NOT EXISTS scenes (id SERIAL PRIMARY KEY, video_id INTEGER NOT NULL, start_frame INTEGER NOT NULL, end_frame INTEGER NOT NULL, embedding real[] NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    database.commit()

    # Insert video
    database.query("INSERT INTO videos (path, name) VALUES (%s, %s) RETURNING id", (video_path, os.path.basename(video_path)))
    video_id = database.fetch_one()[0]
    database.commit()

    # Get video id

    # Insert scenes
    for scene_idx in range(len(scenes)):
        scene = scenes[scene_idx]
        print(scene, flush=True)
        file_name = scene_clip_embeddings[scene_idx]
        vector = load_tensor(file_name).tolist()
        database.query("INSERT INTO scenes (video_id, start_frame, end_frame, embedding) VALUES (%s, %s, %s, %s)", (video_id, scene[0].frame_num, scene[1].frame_num, vector))

    database.commit()
    return 'OK'