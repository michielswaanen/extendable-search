# Masterproef

### Learnings
- SceneDetection quite slow for HD video's
- Optimize by downscaling video first
- Optimize by deleting the saved tensors

### Difficult
- Salsa dancing (full context needs to be known)
- See a table, difficult to know what its made of -> use sound to detect material
- See a child being attacked by a dog -> but when you hear the sound you know that they're playing

### Alternatives
- Look at TimeSformer from facebook


### Learnings
- X-CLIP-BASE:
    - Works great with short videos
    - Works great if you want to find video
    - Doesn't work great for long videos
    - Doesn't work great to find a specific moment in a video
    - Bottleneck: how to process long videos?
        - Maybe use parallel processing
        - Maybe use a different model

# Workings

## 1. Uploading

Given a video, we slice it into smaller videos based on the scene detection algorithm.

~ Q:
- What happens when the video is +1m long and there are no scene changes?

## 2. Indexing

### Visual

Given a scene, we extract the visual features from the video.
When calculating the embedding we supply a list of 8 timestamps.
These 8 timestamps resemble screenshots of the video.
We're using the X-CLIP-BASE model to calculate the embedding based on the 8 screenshots.
Given the embedding, we save it to the database.


### Face

Given a scene, we first detect the faces in the scene.

### Audio

