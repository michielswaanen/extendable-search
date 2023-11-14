from transformers import AutoProcessor, ClapModel
from core.audio.audio_segment import get_audio_as_array, get_sample_rate
import torch
import os

print("Initializing audio model...", flush=True)
processor = AutoProcessor.from_pretrained("laion/clap-htsat-unfused")
model = ClapModel.from_pretrained("laion/clap-htsat-unfused")
print("Model audio initialized", flush=True)

def analyze(job_path, frame_scenes):
    job_scene_path = f'{job_path}/scenes'

    for frames_per_scene in frame_scenes:
        scene_path = f'{job_scene_path}/{frames_per_scene[0]}_{frames_per_scene[-1]}'
        audio_path = f'{scene_path}/audio/audio.wav'

        # Process the audio
        print("> Processing audio {num_scene} of {total_scene} scenes...".format(num_scene=frame_scenes.index(frames_per_scene), total_scene=len(frame_scenes)), flush=True)

        audios = get_audio_as_array(audio_path)

        inputs = processor(audios=audios, return_tensors="pt", sampling_rate=48000)
        embedding = model.get_audio_features(**inputs)

        # Save the embedding to disk
        tensor_path = f'{job_scene_path}/{frames_per_scene[0]}_{frames_per_scene[-1]}/embeddings/'
        os.makedirs(tensor_path, exist_ok=True)
        torch.save(embedding, f'{tensor_path}audio.pt')

    return 'done'