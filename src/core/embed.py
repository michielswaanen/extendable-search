from PIL import Image
from sentence_transformers import SentenceTransformer
import torch
import uuid
import numpy as np
import subprocess

model = SentenceTransformer('model/clip-ViT-B-32')

def embed_image(image: Image):
    embedding = model.encode(image)
    return embedding

def embed_text(text: str):
    embedding = model.encode(text)
    return embedding

def normalize_embedding(embedding):
    return embedding / np.linalg.norm(embedding)

def average_embedding(embed: list):
    return np.mean(embed, axis=0)

def save_tensor(t):
    path = f'/tmp/{uuid.uuid4()}'
    torch.save(t, path)

    return path

def load_tensor(path):
    return torch.load(path)