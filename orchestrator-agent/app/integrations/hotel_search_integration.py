"""Hotel Search Integration Agent"""
import httpx
import json
from typing import Dict, List, Any, Optional
from app.config import settings
from app.logger import logger


class HotelSearchIntegration:
    """Integration with Hotel Search Engine"""

    def __init__(self):
        """Initialize hotel search integration"""
        self.hotel_search_url = settings.hotel_search_url
        self.timeout = 30

    async def search_hotels(
        self,
        query: str,
        num_results: int = 5,
        preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search hotels via Hotel Search Engine API
        
        Args:
            query: Hotel search query
            num_results: Number of results
            preferences: Optional search preferences
            
        Returns:
            Search results from hotel engine
        """
        try:
            logger.info(f"Searching hotels for: {query}")
            
            payload = {
                "query": query,
                "num_results": num_results
            }
            
            # Add preferences if provided
            if preferences:
                payload.update(preferences)
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Check health first
                try:
                    health = await client.get(
                        f"{self.hotel_search_url}/health",
                        timeout=10
                    )
                    logger.debug(f"Hotel Search Service health: {health.status_code}")
                except Exception as health_e:
                    logger.warning(f"Hotel Search Service not available: {str(health_e)}")
                    return {
                        "status": "error",
                        "message": f"Hotel Search Service unavailable: {str(health_e)}",
                        "results": []
                    }
                
                # Send search request
                logger.info(f"Sending request to {self.hotel_search_url}/search")
                response = await client.post(
                    f"{self.hotel_search_url}/search",
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Found {len(result.get('results', []))} hotels")
                    return result
                else:
                    logger.error(f"Hotel Search returned status {response.status_code}")
                    return {
                        "status": "error",
                        "message": f"Hotel Search returned {response.status_code}",
                        "results": []
                    }
        
        except httpx.TimeoutException:
            logger.error("Hotel Search request timed out")
            return {
                "status": "error",
                "message": "Hotel Search request timed out",
                "results": []
            }
        except Exception as e:
            logger.error(f"Hotel search failed: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Hotel search error: {str(e)}",
                "results": []
            }

    async def extract_hotel_preferences(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract hotel preferences from context
        
        Args:
            context: Request context
            
        Returns:
            Hotel preferences dict
        """
        preferences = {}
        
        if "min_rating" in context:
            preferences["min_rating"] = context["min_rating"]
        if "max_price" in context:
            preferences["max_price"] = context["max_price"]
        if "amenities" in context:
            preferences["amenities"] = context["amenities"]
        if "location" in context:
            preferences["location"] = context["location"]
        
        return preferences

    def format_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format results for LLM context"""
        return results.get("results", [])
