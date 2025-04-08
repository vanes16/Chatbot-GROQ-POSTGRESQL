import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.db_models import ChatbotData

class DatabaseOperations:
    @staticmethod
    async def vector_search(
        session: AsyncSession,
        embedding_vector: List[float],
        threshold: float = 0.8,
        limit: int = 5,
        pre_filter: Optional[dict] = None
    ) -> List[ChatbotData]:
        """
        Optimized vector search with pre-filtering capabilities
        
        Args:
            session: Async database session
            embedding_vector: Embedding vector to compare with
            threshold: Similarity threshold (0.8 default)
            limit: Maximum number of results
            pre_filter: Dictionary of column filters to apply before vector search
                       Example: {"category": "general", "language": "id"}
        """
        max_distance = 1 - threshold
        
        # Base query
        query = select(ChatbotData)
        
        # Apply pre-filters if provided
        if pre_filter:
            for column, value in pre_filter.items():
                query = query.where(getattr(ChatbotData, column) == value)
        
        # Apply vector search
        query = (
            query.order_by(ChatbotData.embedding_vector.cosine_distance(embedding_vector))
            .where(ChatbotData.embedding_vector.cosine_distance(embedding_vector) <= max_distance)
            .limit(limit)
        )
        
        try:
            result = await session.execute(query)
            return result.scalars().all()
        except Exception as error:
            raise RuntimeError(f"Vector search error: {str(error)}") from error

    @staticmethod
    async def hybrid_search(
        session: AsyncSession,
        query_text: str,
        embedding_model,
        threshold: float = 0.8,
        limit: int = 5,
        pre_filter: Optional[dict] = None
    ) -> List[ChatbotData]:
        """
        Optimized hybrid search with text-to-embedding conversion
        
        Args:
            pre_filter: Additional filters to apply before vector search
        """
        try:
            embedding = await asyncio.to_thread(embedding_model.get_embedding, query_text)
            return await DatabaseOperations.vector_search(
                session, 
                embedding, 
                threshold, 
                limit,
                pre_filter
            )
        except Exception as error:
            raise RuntimeError(f"Hybrid search error: {str(error)}") from error