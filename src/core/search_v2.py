from transformers import AutoModel, AutoTokenizer

def handle_search(request):

    # Get search query from body
    query = request.json['query']

    tokenizer = AutoTokenizer.from_pretrained("microsoft/xclip-base-patch32")
    model = AutoModel.from_pretrained("microsoft/xclip-base-patch32")

    inputs = tokenizer([query], padding=True, return_tensors="pt")
    text_features = model.get_text_features(**inputs)

    embedding = text_features[0].tolist()

    return embedding
