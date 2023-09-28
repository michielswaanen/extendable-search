from PIL import Image
from sentence_transformers import SentenceTransformer
import torch
import uuid
import numpy as np

model = SentenceTransformer('model/clip-ViT-B-32')

def embed_normalize(image: Image):
    embedding = model.encode(image)
    return normalize_embedding(embedding).tolist()

def embed(src):
    embedding = model.encode(src)
    return embedding

def normalize_embedding(embedding):
    # return embedding
    return embedding
    # return embedding / np.linalg.norm(embedding)

def average_embedding(embed: list):
    return np.mean(embed, axis=0)

def save_tensor(t):
    path = f'/tmp/{uuid.uuid4()}'
    torch.save(t, path)

    return path

def load_tensor(path):
    return torch.load(path)