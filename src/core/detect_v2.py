import av
import torch
import numpy as np
from transformers import AutoProcessor, AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download
from core.database import Database
import os
import scenedetect as sd
import cv2

# np.random.seed(0)

print("Initializing model...", flush=True)
processor = AutoProcessor.from_pretrained("microsoft/xclip-base-patch32")
model = AutoModel.from_pretrained("microsoft/xclip-base-patch32")
print("Model initialized", flush=True)

def read_video_pyav(container, indices):
    '''
    Decode the video with PyAV decoder.
    Args:
        container (`av.container.input.InputContainer`): PyAV container.
        indices (`List[int]`): List of frame indices to decode.
    Returns:
        result (np.ndarray): np array of decoded frames of shape (num_frames, height, width, 3).
    '''

    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]

    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)

    print ("frames", frames, flush=True)

    return np.stack([x.to_ndarray(format="rgb24") for x in frames], axis=0)


def sample_frame_indices(clip_len, frame_sample_rate, seg_len):
    '''
    Sample a given number of frame indices from the video.
    Args:
        clip_len (`int`): Total number of frames to sample.
        frame_sample_rate (`int`): Sample every n-th frame.
        seg_len (`int`): Maximum allowed index of sample's last frame.

    Returns:
        indices (`List[int]`): List of sampled frame indices
    '''

    print("(param) clip_len", clip_len, flush=True)
    print("(param) frame_sample_rate", frame_sample_rate, flush=True)
    print("(param) seg_len", seg_len, flush=True)
    converted_len = int(clip_len * frame_sample_rate)
    print("converted_len", converted_len, flush=True)
    end_idx = np.random.randint(converted_len, seg_len)
    print("end_idx", end_idx, flush=True)
    start_idx = end_idx - converted_len
    print("start_idx", start_idx, flush=True)
    indices = np.linspace(start_idx, end_idx, num=clip_len)
    print("indices", indices, flush=True)
    indices = np.clip(indices, start_idx, end_idx - 1).astype(np.int64)
    print("indices overwrite", indices, flush=True)

    return indices

def detect_scenes(video_path):
    video = sd.open_video(video_path)

    sm = sd.SceneManager()

    sm.add_detector(sd.ContentDetector(threshold=27.0))
    sm.detect_scenes(video)

    scenes = sm.get_scene_list()

    every_n = 2 # number of samples per scene
    no_of_samples = 8 # number of samples per scene

    scenes_frame_samples = []

    for scene_idx in range(len(scenes)):
        scene_length = abs(scenes[scene_idx][0].frame_num - scenes[scene_idx][1].frame_num)
        print("scene_length", scene_length, flush=True)
        every_n = round(scene_length/no_of_samples)
        local_samples = [(every_n * n) + scenes[scene_idx][0].frame_num for n in range(no_of_samples)]

        scenes_frame_samples.append(local_samples)

    print(scenes_frame_samples, flush=True)
    return scenes_frame_samples

def get_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    return fps

# This should lower the dimensions of the video and save it to a new file
def lower_dimensions(video_path):



def handle_detect(video_name):
    video_path = 'code/uploads/{filename}'.format(filename=video_name)
    container = av.open(video_path)

    # sample 8 frames
    scenes = detect_scenes(video_path)

    # Round up to nearest 3
    fps = round(get_fps(video_path), 3)

    video_features = []

    for scene in scenes:
        # indices = sample_frame_indices(clip_len=8, frame_sample_rate=10, seg_len=container.streams.video[0].frames)
    # print("indices", indices, flush=True)
        video = read_video_pyav(container, scene)
        print("Processing video a total of {indices} frames...".format(indices=len(scene)), flush=True)
        inputs = processor(videos=list(video), return_tensors="pt")
        print("Calculating features...", flush=True)
        video_features.append(model.get_video_features(**inputs))

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

    print('Connected to database', flush=True)

    # Create vector extension
    database.query("CREATE TABLE IF NOT EXISTS videos (id SERIAL PRIMARY KEY, path VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, fps NUMERIC(3) NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    database.query("CREATE TABLE IF NOT EXISTS scenes (id SERIAL PRIMARY KEY, video_id INTEGER NOT NULL, start_frame INTEGER NOT NULL, end_frame INTEGER NOT NULL, embedding VECTOR(512) NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
    database.query("CREATE EXTENSION IF NOT EXISTS vector SCHEMA scenes")
    database.query("CREATE INDEX ON scenes USING hnsw (embedding vector_cosine_ops)")
    database.commit()

    # Insert video
    database.query("INSERT INTO videos (path, name, fps) VALUES (%s, %s, %s) RETURNING id", (video_path, video_path, fps))
    video_id = database.fetch_one()
    print ("video_id", video_id, flush=True)
    database.commit()


    # Get embedding from tensor

    for scene in scenes:
        embedding = video_features[scenes.index(scene)][0].tolist()
        database.query("INSERT INTO scenes (video_id, start_frame, end_frame, embedding) VALUES (%s, %s, %s, %s)", (video_id, scene[0], scene[-1], embedding))

    database.commit()

    return 'OK'