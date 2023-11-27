from deepface import DeepFace
import cv2
import numpy as np
import tempfile
import os
from core.database.database import Database
import time

def handle_face(request):

    def detect_faces(img):
        start = time.time()
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
            face_path = f'{path}face_{index}.jpg';
            cv2.imwrite(face_path, cropped)
            embedding = embed_face(face_path)
            save_face_embedding(embedding, face_path)
            index += 1

        end = time.time()

        print(f'Elapsed time: {end - start}', flush=True)


        return "OK"

    def embed_face(img):
        res =  DeepFace.represent(img_path=img, model_name ='Facenet', enforce_detection=False)
        # print(res, flush=True)
        return res[0]['embedding']

    def save_face_embedding(embedding, face_path):
        # Init database
        database = Database(
            uri=os.getenv('DATABASE_URI')
        )

        print('Connecting to database', flush=True)

        # Connect to database
        database.connect()

        print('Saving to database...', flush=True)
        database.query("INSERT INTO faces (embedding, file_name) VALUES (%s, %s)", (str(embedding), face_path))
        database.commit()
        print('Saved to database', flush=True)

        pass


    detect_faces('code/uploads/faces/IMG-20220716-WA0003.jpg')
    detect_faces('code/uploads/faces/IMG-20221127-WA0000.jpg')
    detect_faces('code/uploads/faces/IMG-20220807-WA0000.jpg')

    return 'OK'