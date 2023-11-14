import cv2

def get_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    return fps

def get_duration(video_path):
    cap = cv2.VideoCapture(video_path)
    duration = cap.get(cv2.CAP_PROP_POS_MSEC)
    return duration