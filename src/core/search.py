from core.embed import embed_text

def handle_search(request):

    # Get search query from body
    query = request.json['query']

    # Embed query
    query_embedding = embed_text(query)

    print(query_embedding, flush=True)

    return 'Search query received'