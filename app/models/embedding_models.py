from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self):
        # Gunakan model yang sesuai dengan dimensi contoh 1024 untuk sentencetransformers
        self.model = SentenceTransformer('all-roberta-large-v1')  

    def get_embedding(self, text: str):
        return self.model.encode(text).tolist()