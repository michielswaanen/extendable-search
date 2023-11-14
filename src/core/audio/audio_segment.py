from pydub import AudioSegment
from pydub.utils import mediainfo

def segment_audio(start_time, end_time, audio_path):
    audio = AudioSegment.from_mp3(audio_path)
    audio = audio[start_time:end_time]
    return audio

def get_audio_as_array(audio_path):
    audio = AudioSegment.from_mp3(audio_path)
    audio.set_frame_rate(48000)
    return audio.get_array_of_samples()

def get_sample_rate(audio_path):
    info = mediainfo(audio_path)
    return info['sample_rate']