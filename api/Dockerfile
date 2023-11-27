FROM python:3.11-bullseye

WORKDIR /app

RUN apt-get clean && \
    apt-get update -y && \
    apt-get upgrade -y && \
    # Install Git dependencies
    apt-get install git git-lfs \
    # Install OpenCV dependencies
    ffmpeg libsm6 libxext6 -y && \
    git-lfs install && \
    git clone https://huggingface.co/sentence-transformers/clip-ViT-B-32 && \
    mkdir model && \
    mv clip-ViT-B-32 model/clip-ViT-B-32


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python" ]
