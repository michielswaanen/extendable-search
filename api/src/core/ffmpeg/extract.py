import numpy as np

def extract_screenshot(container, frame_num):
    '''
    Decode the video with PyAV decoder.
    Args:
        container (`av.container.input.InputContainer`): PyAV container.
        indices (`List[int]`): List of frame indices to decode.
    Returns:
        result (np.ndarray): np array of decoded frames of shape (num_frames, height, width, 3).
    '''

    try:
        framerate = container.streams.video[0].average_rate
        time_base = container.streams.video[0].time_base
        sec = int(frame_num/framerate)

        # Seek gives back the nearest key frame
        container.seek(sec*1000000, whence='time', backward=True)

        # Get the next available frame
        frame = next(container.decode(video=0))

        # Get the proper key frame number
        sec_frame = int(frame.pts * time_base * framerate)

        for _ in range(sec_frame, frame_num):
            frame = next(container.decode(video=0))

        result = frame.to_ndarray(format="rgb24")
    except StopIteration:
        print(f"> Could not extract frame {frame}", flush=True)
        result = None

    return result