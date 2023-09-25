import os
import scenedetect as sd
import cv2
from PIL import Image
from transformers import CLIPProcessor
import torch
import uuid
from core.database import Database
from dotenv import load_dotenv

clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
load_dotenv()

def clip_embeddings(image):
    inputs = clip_processor(images=image, return_tensors="pt", padding=True)
    input_tokens = {
        k: v for k, v in inputs.items()
    }

    return input_tokens['pixel_values']

def save_tensor(t):
    path = f'/tmp/{uuid.uuid4()}'
    torch.save(t, path)

    return path

def load_tensor(path):
    return torch.load(path)

def handle_detect(video_path):

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
    no_of_samples = 5 # number of samples per scene

    scenes_frame_samples = []

    for scene_idx in range(len(scenes)):
        scene_length = abs(scenes[scene_idx][0].frame_num - scenes[scene_idx][1].frame_num)
        every_n = round(scene_length/no_of_samples)
        local_samples = [(every_n * n) + scenes[scene_idx][0].frame_num for n in range(3)]

        scenes_frame_samples.append(local_samples)

    print(scenes_frame_samples, flush=True)

    ##############################
    #         Embedding          #
    ##############################

    scene_clip_embeddings = [] # to hold the scene embeddings in the next step

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

            clip_pixel_values = clip_embeddings(pil_image)

            pixel_tensors.append(clip_pixel_values)

        avg_tensor = torch.mean(torch.stack(pixel_tensors), dim=0)
        scene_clip_embeddings.append(save_tensor(avg_tensor))

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
    database.query("INSERT INTO videos (path, name) VALUES (%s, %s)", (video_path, os.path.basename(video_path)))
    database.commit()

    # Insert scenes
    for scene_idx in range(len(scenes)):
        scene = scenes[scene_idx]
        print(scene, flush=True)
        file_name = scene_clip_embeddings[scene_idx]
        vector = load_tensor(file_name).tolist()
        database.query("INSERT INTO scenes (video_id, start_frame, end_frame, embedding) VALUES (%s, %s, %s, %s)", (1, scene[0].frame_num, scene[1].frame_num, vector))

    database.commit()
    return 'OK'