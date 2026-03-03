"""Hotel Search Integration Agent"""

import httpx
from typing import Dict, List, Any, Optional
from app.config import settings
from app.logger import logger
from app.exceptions import AgentIntegrationError


class HotelSearchIntegration:
    """Integration with Hotel Search Engine"""

    def __init__(self) -> None:
        self.base_url = settings.hotel_search_url
        self.timeout = httpx.Timeout(
            connect=5.0,
            read=30.0,
            write=5.0,
            pool=5.0,
        )

        # Persistent connection (pooling enabled)
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
        )

    async def search_hotels(
        self,
        query: str,
        num_results: int = 5,
        preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Search hotels via Hotel Search Engine API"""

        logger.info(f"[HotelSearchEngine] Searching for: {query}")

        payload = {
            "query": query,
            "num_results": num_results,
        }

        if preferences:
            payload.update(preferences)

        try:
            response = await self.client.post("/search", json=payload)

            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            logger.info(f"[HotelSearchEngine] Found {len(results)} hotels")

            return {
                "status": "success",
                "results": results,
            }

        except httpx.TimeoutException:
            logger.error("[HotelSearchEngine] Request timed out")
            raise AgentIntegrationError("Hotel Search Engine timeout")

        except httpx.HTTPStatusError as e:
            logger.error(
                f"[HotelSearchEngine] HTTP error {e.response.status_code}"
            )
            raise AgentIntegrationError(
                f"Hotel Search Engine returned {e.response.status_code}"
            )

        except Exception as e:
            logger.error(
                f"[HotelSearchEngine] Unexpected error: {str(e)}",
                exc_info=True,
            )
            raise AgentIntegrationError("Hotel Search Engine failure")

    async def extract_hotel_preferences(
        self,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Extract hotel preferences from context"""

        preferences: Dict[str, Any] = {}

        if "min_rating" in context:
            preferences["min_rating"] = context["min_rating"]

        if "max_price" in context:
            preferences["max_price"] = context["max_price"]

        if "amenities" in context:
            preferences["amenities"] = context["amenities"]

        if "location" in context:
            preferences["location"] = context["location"]

        return preferences

    def format_results(
        self,
        results: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Format results for LLM context"""
        return results.get("results", [])

    async def close(self) -> None:
        """Close HTTP client"""
        await self.client.aclose()