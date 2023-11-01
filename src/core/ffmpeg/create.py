import subprocess

def create_downscaled_video_copy(input_path, output_path, scale='480'):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vcodec', 'copy', # copy video stream
        '-vf', 'scale=480:-1', # scale height to 480p
        # '-r', '10', # reduce frame rate to 10 fps (better results with native frame rate)
        '-c:v', 'libx264', # use the h.264 codec
        '-crf', '18', # set visual compression level (0: loseless, 51: worst)
        '-preset', 'ultrafast', # veryslow: smaller file size, but takes longer to compress
        '-an', # remove audio stream
        output_path
    ]

    print(f"> Creating a downscaled video copy at {output_path}...", flush=True)
    subprocess.call(command, stdout = subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # subprocess.run(command)
    print(f"> Finished creating a downscaled video copy at {output_path}", flush=True)

    return output_path

def create_audio_copy(input_path, output_path):
    command = [
        'ffmpeg',
        '-i', input_path,
        '-vn', # remove video stream
        '-acodec', 'libmp3lame', # use mp3 codec
        '-ac', '2', # set audio channels to stereo
        '-ab', '160k', # set audio bitrate to 160k
        '-ar', '48000', # set audio sampling rate to 48kHz
        '-f', 'mp3',
        output_path
    ]

    print(f"> Creating an audio copy at {output_path}...", flush=True)
    subprocess.call(command, stdout = subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # subprocess.run(command)
    print(f"> Finished creating an audio copy at {output_path}", flush=True)

    return output_path