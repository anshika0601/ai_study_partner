from lanchain.embeddings import HuggingFaceEmbeddings

def get_embeddings():
    model="sentence-transformers/all-MiniLM-L6-v2"
    return HuggingFaceEmbeddings(model_name=model)