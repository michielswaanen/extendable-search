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