FROM python:3.11.5-bullseye

WORKDIR /app

# OpenCV dependencies
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6
# RUN apk update && \
#     apk upgrade && \
#     apk add \
#     opencv
#     # ffmpeg \
#     # libsm-dev \
#     # libxrender \
#     # libxext-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python" ]