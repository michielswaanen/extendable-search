import numpy as np

def extract_scene(container, frames_per_scene):
    '''
    Decode the video with PyAV decoder.
    Args:
        container (`av.container.input.InputContainer`): PyAV container.
        indices (`List[int]`): List of frame indices to decode.
    Returns:
        result (np.ndarray): np array of decoded frames of shape (num_frames, height, width, 3).
    '''

    frames = []

    for i in frames_per_scene:
        try:
            print(f"> Extracting frame {i}", flush=True)
            container.seek(i, any_frame=True)
            frame = next(container.decode(video=0))
            frames.append(frame)
        except StopIteration:
            print(f"> Could not extract frame {i}", flush=True)
            break

    result = np.stack([x.to_ndarray(format="rgb24") for x in frames], axis=0)

    print("> Finished extracting frames", flush=True)

    return result