import av
import torch
import numpy as np
from transformers import AutoProcessor, AutoModel, AutoTokenizer
from huggingface_hub import hf_hub_download
from core.database import Database
import os

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

def handle_detect(video_path):
    container = av.open('code/uploads/{filename}'.format(filename=video_path))

    # sample 8 frames
    print("container", container, flush=True)
    indices = sample_frame_indices(clip_len=8, frame_sample_rate=10, seg_len=container.streams.video[0].frames)
    print("indices", indices, flush=True)
    video = read_video_pyav(container, indices)

    print("Processing video a total of {indices} frames...".format(indices=len(indices)), flush=True)
    inputs = processor(videos=list(video), return_tensors="pt")
    print("Calculating features...", flush=True)
    video_features = model.get_video_features(**inputs)

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

    # Get embedding from tensor
    embedding = video_features[0].tolist()

    database.query("INSERT INTO scenes (video_id, start_frame, end_frame, embedding) VALUES (%s, %s, %s, %s)", (video_id, 0, 1, embedding))
    database.commit()

    return 'OK'