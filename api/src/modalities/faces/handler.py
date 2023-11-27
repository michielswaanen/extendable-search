import os
from deepface import DeepFace
import cv2
import torch

def embed_face(img):
    res =  DeepFace.represent(img_path=img, model_name ='VGG-Face', enforce_detection=False)
    return res[0]['embedding']

def analyze(job_path, frame_scenes):
    scenes_path = f'{job_path}/scenes'

    for frames_per_scene in frame_scenes:
        scene_path = f'{scenes_path}/{frames_per_scene[0]}_{frames_per_scene[-1]}'
        shots_folder = f'{scene_path}/shots/'
        faces_folder = f'{scene_path}/faces/'
        embeddings_folder = f'{scene_path}/embeddings/'

        # Grab all the images in the screenshot folder
        screenshots = os.listdir(shots_folder)

        if not os.path.exists(faces_folder):
            os.makedirs(faces_folder)

        for screenshot in screenshots:
            shot_path = f'{shots_folder}{screenshot}'

            faces = DeepFace.extract_faces(img_path=shot_path, detector_backend='ssd', target_size = (224, 224), enforce_detection=False)

            found_faces = len(faces) > 1 or (len(faces) == 1 and faces[0]['facial_area']['x'] > 0 and faces[0]['facial_area']['y'] > 0)

            if found_faces:
                faces = DeepFace.extract_faces(img_path=shot_path, detector_backend='retinaface', target_size = (224, 224), enforce_detection=False)

                image = cv2.imread(shot_path)
                index = 0

                for face in faces:
                    area = face['facial_area']
                    x = area['x']
                    y = area['y']
                    w = area['w']
                    h = area['h']
                    cropped = image[y:y + h, x:x + w]
                    face_path = f'{faces_folder}{index}.jpg';
                    cv2.imwrite(face_path, cropped)
                    index += 1

                print(f'Found {len(faces)} faces in {shot_path}', flush=True)

                # Save the embedding to disk
                os.makedirs(embeddings_folder, exist_ok=True)

                # Loop over the saved faces and embed them
                for index in range(len(faces)):
                    embedding = embed_face(faces_folder + f'{index}.jpg')
                    print(f'Embedding shape: {len(embedding)}', flush=True)
                    torch.save(embedding, f'{embeddings_folder}face_{index}.pt')

                # If one face is found, stop looking for faces in this scene
                # This is most likely a face that is clearly visible otherwise ssd wouldn't have found it
                break
            else:
                print(f'No faces found in {shot_path}', flush=True)
