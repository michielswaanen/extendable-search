from transformers import AutoModel, AutoTokenizer
from core.database.database import Database
import os

def generate_embedding(request):
    query = request.json['query']

    tokenizer = AutoTokenizer.from_pretrained("microsoft/xclip-base-patch32")
    model = AutoModel.from_pretrained("microsoft/xclip-base-patch32")

    inputs = tokenizer([query], padding=True, return_tensors="pt")
    text_features = model.get_text_features(**inputs)

    return text_features[0].tolist()

def handle_output(result: list):
    output = []

    for scene in result:
        output.append({
            'name': scene[0],
            'similarity': scene[4],
            'start_time': {
                'minutes': int(scene[1] / (scene[3] * 60)),
                'seconds': int(scene[1] / scene[3]) % 60,
            },
            'end_time': {
                'minutes': int(scene[2] / (scene[3] * 60)),
                'seconds': int(scene[2] / scene[3]) % 60,
            }
        })

    return output

def handle_search(request):

    print("Generating embedding...", flush=True)
    embedding = generate_embedding(request)
    print("Embedding generated!", flush=True)

    database = Database(
        uri=os.getenv('DATABASE_URI')
    )

    print('Connecting to database', flush=True)
    database.connect()

    database.query("SELECT videos.name, scenes.start_frame, scenes.end_frame, videos.fps, 1 - (scenes.embedding <=> %s) as similarity FROM scenes INNER JOIN videos ON scenes.video_id = videos.id WHERE 1 - (embedding <=> %s) > %s ORDER BY similarity DESC LIMIT 5", (str(embedding), str(embedding), 0.1))

    print("Fetching results...", flush=True)
    results = database.fetch_all()
    print("Fetching results!", len(results), flush=True)
    database.commit()

    return handle_output(results)

# ffmpeg -i one-minute.mp4 -vf scale=480:-1 -r 10 one-minute-480-3.mp4
