from transformers import AutoProcessor, AutoModel, AutoTokenizer
import av
import torch
from core.ffmpeg.extract import extract_scene
import numpy as np
import os

print("Initializing model...", flush=True)
processor = AutoProcessor.from_pretrained("microsoft/xclip-base-patch32")
model = AutoModel.from_pretrained("microsoft/xclip-base-patch32")
print("Model initialized", flush=True)

def analyze(job_path, frame_scenes):
    ds_video = f'{job_path}/original.mp4'
    job_scene_path = f'{job_path}/scenes'
    container = av.open(ds_video)


    for frames_per_scene in frame_scenes:
        print("> Processing {num_scene} of {total_scene} scenes...".format(num_scene=frame_scenes.index(frames_per_scene), total_scene=len(frame_scenes)), flush=True)
        video = extract_scene(container, frames_per_scene)
        inputs = processor(videos=list(video), return_tensors="pt")
        embedding = model.get_video_features(**inputs)
        # print("embedding", embedding, flush=True)

        # Save embedding to text file
        tensor_path = f'{job_scene_path}/{frames_per_scene[0]}_{frames_per_scene[-1]}/tensors/'
        os.makedirs(tensor_path, exist_ok=True)
        torch.save(embedding, f'{tensor_path}embedding.pt')

    return 'done'