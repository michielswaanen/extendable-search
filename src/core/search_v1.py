from core.embed import embed_normalize

def handle_search(request):

    # Get search query from body
    query = request.json['query']

    return embed_normalize(query)