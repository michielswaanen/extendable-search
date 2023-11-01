import tempfile
import os

def save_job_on_disk(video):
    temp_dir = tempfile.TemporaryDirectory()
    job_path = f'code/jobs{temp_dir.name}/'
    os.makedirs(job_path)

    video_path = f'{job_path}original.mp4'
    video.save(video_path)

    return job_path