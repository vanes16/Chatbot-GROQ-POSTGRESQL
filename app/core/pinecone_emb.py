# import os
# from pinecone import Pinecone  # Impor class Pinecone
# from dotenv import load_dotenv
# from app.models.embedding_models import EmbeddingModel

# load_dotenv()

# # Inisialisasi Pinecone
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))  # Gunakan class Pinecone

# # Inisialisasi model embedding
# embedding_model = EmbeddingModel()

# class PineconeIntegration:
#     def __init__(self):
#         self.index_name = os.getenv("PINECONE_INDEX_NAME")
#         if self.index_name not in pc.list_indexes().names():  # Perhatikan penggunaan .names()
#             # Buat index baru jika belum ada
#             pc.create_index(
#                 name=self.index_name,
#                 dimension=1024,  # Sesuaikan dengan dimensi embedding
#                 metric="cosine"  # Metrik untuk similarity search
#             )
#         self.index = pc.Index(self.index_name)

#     def upsert_embedding(self, id: str, question: str, answer: str, metadata: dict = {}):
#         """Menyimpan embedding pertanyaan dan jawaban ke Pinecone."""
#         embedding = embedding_model.get_embedding(question)
#         self.index.upsert([(id, embedding, {"answer": answer, **metadata})])

#     def query_embedding(self, question: str, top_k: int = 5):
#         """Mencari jawaban yang paling relevan berdasarkan embedding pertanyaan."""
#         embedding = embedding_model.get_embedding(question)
#         results = self.index.query(vector=embedding, top_k=top_k, include_metadata=True)
#         return results
