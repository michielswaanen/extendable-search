from deepface import DeepFace
import cv2
import numpy as np
import tempfile
import os

def handle_face(request):

    def detect_faces(img):
        temp_dir = tempfile.TemporaryDirectory()
        path = f'code/uploads/faces{temp_dir.name}/'
        os.makedirs(path)

        faces = DeepFace.extract_faces(img_path=img, detector_backend='retinaface', target_size = (224, 224), align = True)
        image = cv2.imread(img)

        index = 0
        for face in faces:
            area = face['facial_area']
            x = area['x']
            y = area['y']
            w = area['w']
            h = area['h']
            cropped = image[y:y + h, x:x + w]
            face_path = f'{path}/face_{index}.jpg';
            cv2.imwrite(face_path, cropped)
            embed_face(face_path)
            index += 1

        return "OK"

    def embed_face(img):
        faces = DeepFace.represent(img_path=img, model_name ='Facenet512', enforce_detection=False)
        print(faces, flush=True)
        return "OK"


    return detect_faces('code/uploads/faces/IMG-20220716-WA0003.jpg')