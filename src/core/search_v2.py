from transformers import AutoModel, AutoTokenizer
from core.database import Database
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
            'start_time': scene[1] / float(scene[3]),
            'end_time': scene[2] / float(scene[3])
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

    database.query("SELECT videos.name,  scenes.start_frame, scenes.end_frame, videos.fps FROM scenes INNER JOIN videos ON scenes.video_id = videos.id ORDER BY embedding <-> %s LIMIT 5", (str(embedding),))
    print("Fetching results...", flush=True)
    results = database.fetch_all()
    print("Fetching results!", flush=True)
    database.commit()

    return handle_output(results)
