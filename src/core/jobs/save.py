import tempfile
import os

def save_job_on_disk(video):
    temp_dir = tempfile.TemporaryDirectory()
    job_id = temp_dir.name.split('/')[-1]
    job_path = f'code/jobs/{job_id}'
    os.makedirs(job_path)

    video_path = f'{job_path}/original.mp4'
    video.save(video_path)

    return job_id, video_path