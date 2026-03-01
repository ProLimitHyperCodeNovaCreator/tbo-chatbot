"""RAG Engine - Retrieval Augmented Generation from Qdrant Vector DB"""
import httpx
import json
from typing import List, Dict, Any, Optional
from app.config import settings
from app.logger import logger


class RAGEngine:
    """Retrieve data from Qdrant Vector DB and augment LLM context"""

    def __init__(self):
        """Initialize RAG engine"""
        self.qdrant_host = settings.qdrant_host
        self.qdrant_port = settings.qdrant_port
        self.qdrant_url = f"http://{self.qdrant_host}:{self.qdrant_port}"
        self.timeout = 30

    async def search_travel_data(
        self,
        query: str,
        collection: str = "travel_data",
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search vector DB for relevant travel data
        
        Args:
            query: Search query
            collection: Qdrant collection name
            limit: Max results to return
            
        Returns:
            List of relevant travel data documents
        """
        try:
            logger.info(f"Searching Qdrant for: {query}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Check if Qdrant is available
                try:
                    health_response = await client.get(f"{self.qdrant_url}/readyz")
                    logger.debug(f"Qdrant health: {health_response.status_code}")
                except Exception as health_e:
                    logger.warning(f"Qdrant not available: {str(health_e)}")
                    return []
                
                # Try to search in collection
                try:
                    response = await client.get(
                        f"{self.qdrant_url}/collections/{collection}",
                        timeout=self.timeout
                    )
                    if response.status_code == 404:
                        logger.warning(f"Collection '{collection}' not found in Qdrant")
                        return []
                except Exception as e:
                    logger.warning(f"Could not check collection: {str(e)}")
                    return []
            
            # Return empty for now - Qdrant search would be implemented here
            # with actual vector embedding and search
            logger.info("RAG: No results yet (vector search pending implementation)")
            return []
            
        except Exception as e:
            logger.error(f"RAG search failed: {str(e)}")
            return []

    async def retrieve_context(
        self,
        query: str,
        hotel_data: Optional[List[Dict[str, Any]]] = None,
        travel_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Build comprehensive context for LLM
        
        Args:
            query: User query
            hotel_data: Hotel search results
            travel_data: Travel package data from Qdrant
            
        Returns:
            Context dict with all relevant data
        """
        context = {
            "query": query,
            "hotel_data": hotel_data or [],
            "travel_data": travel_data or [],
            "sources": []
        }
        
        if hotel_data:
            context["sources"].append("hotel_search_engine")
        if travel_data:
            context["sources"].append("qdrant_vectordb")
            
        logger.info(f"Built RAG context with sources: {context['sources']}")
        return context

    def format_for_llm(self, context: Dict[str, Any]) -> str:
        """Format context data for LLM prompt"""
        formatted = f"Query: {context['query']}\n\n"
        
        if context.get("hotel_data"):
            formatted += "=== Hotel Search Results ===\n"
            for i, hotel in enumerate(context["hotel_data"][:3], 1):
                formatted += f"{i}. {hotel.get('name', 'Unknown')}\n"
                if "rating" in hotel:
                    formatted += f"   Rating: {hotel['rating']}/5\n"
                if "price_per_night" in hotel:
                    formatted += f"   Price: ${hotel['price_per_night']}/night\n"
                if "location" in hotel:
                    formatted += f"   Location: {hotel['location']}\n"
            formatted += "\n"
        
        if context.get("travel_data"):
            formatted += "=== Travel Package Data ===\n"
            for i, package in enumerate(context["travel_data"][:3], 1):
                formatted += f"{i}. {json.dumps(package, indent=2)}\n"
            formatted += "\n"
        
        formatted += "Based on the above data, provide a comprehensive response:\n"
        return formatted
