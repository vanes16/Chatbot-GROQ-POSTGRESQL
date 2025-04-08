from typing import Optional, List
from app.models.embedding_models import EmbeddingModel
from app.database.database_operation import DatabaseOperations
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.groq_integration import GroqIntegration  

async def get_chatbot_response(
    user_input: str,
    db_session: AsyncSession,
    threshold: float = 0.8,
    primary_groq_model: str = "llama3-70b-8192",
    fallback_models: List[str] = ["deepseek-r1-distill-llama-70b", "mistral-saba-24b"]
) -> str:
    try:
        embedding_model = EmbeddingModel()
        embedding = embedding_model.get_embedding(user_input)
        
        results = await DatabaseOperations.vector_search(
            session=db_session,
            embedding_vector=embedding,
            threshold=threshold,
            limit=1
        )

        if results:
            return results[0].answer
        
    except Exception as e:
        pass  # Akan dilanjutkan ke fallback Groq
    
    # Jika tidak ditemukan di database atau error, gunakan Groq
    groq = GroqIntegration()
    prompt = f"{user_input}. Berikan jawaban yang singkat tapi relevan"
    
    # Coba model utama terlebih dahulu
    try:
        groq_response = groq.query_groq(model=primary_groq_model, prompt=prompt)
        if groq_response:
            return groq_response
    except Exception as e:
        pass  
    
    # Coba model-model fallback secara berurutan
    for model in fallback_models:
        try:
            groq_response = groq.query_groq(model=model, prompt=prompt)
            if groq_response:
                return groq_response
        except Exception as e:
            continue
    
    # Jika semua model gagal
    return "Maaf, saya mengalami kesalahan saat mencari jawaban dan semua model fallback tidak tersedia."