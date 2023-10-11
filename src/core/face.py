from deepface import DeepFace
import cv2
import numpy as np

def handle_face(request):

    # Detect face
    # https://pypi.org/project/deepface/

    def detect_face(img):
        detector = cv2.dnn.readNetFromCaffe(
            'code/src/models/deploy.prototxt.txt', 'code/src/models/res10_300x300_ssd_iter_140000.caffemodel')

        face_cascade = cv2.CascadeClassifier('code/src/models/haarcascade_frontalface_default.xml')

        image = cv2.imread(img)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            faces = image[y:y + h, x:x + w]
            cv2.imwrite(f'code/uploads/faces/extracted/face{x}_{y}_{w}_{h}.jpg', faces)

        return "OK"

    return detect_face('code/uploads/faces/IMG-20190420-WA0005.jpg')