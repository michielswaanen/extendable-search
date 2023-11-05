from transformers import AutoProcessor, AutoModel, AutoTokenizer
import av
import torch
from core.ffmpeg.extract import extract_scene
import numpy as np
import os
from PIL import Image

print("Initializing model...", flush=True)
processor = AutoProcessor.from_pretrained("microsoft/xclip-base-patch32")
model = AutoModel.from_pretrained("microsoft/xclip-base-patch32")
print("Model initialized", flush=True)

def analyze(job_path, frame_scenes):
    job_scene_path = f'{job_path}/scenes'

    for frames_per_scene in frame_scenes:
        scene_path = f'{job_scene_path}/{frames_per_scene[0]}_{frames_per_scene[-1]}'
        screenshots_path = f'{scene_path}/shots/'

        # Grab all the images in the screenshot folder
        images = os.listdir(screenshots_path)

        # Convert images to a stack of ndarray
        frames = []

        for image in images:
            img = Image.open(f'{screenshots_path}{image}')
            frames.append(np.array(img))

        frames = np.stack(frames, axis=0)

        # Process the frames
        print("> Processing {num_scene} of {total_scene} scenes...".format(num_scene=frame_scenes.index(frames_per_scene), total_scene=len(frame_scenes)), flush=True)

        inputs = processor(videos=list(frames), return_tensors="pt")
        embedding = model.get_video_features(**inputs)

        # Save the embedding to disk
        tensor_path = f'{job_scene_path}/{frames_per_scene[0]}_{frames_per_scene[-1]}/tensors/'
        os.makedirs(tensor_path, exist_ok=True)
        torch.save(embedding, f'{tensor_path}embedding.pt')

    return 'done'