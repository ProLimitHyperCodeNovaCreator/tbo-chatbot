"""Integration with Hotel Search Agent"""

import httpx
from typing import Dict, Any, List, Optional
from app.config import settings
from app.logger import logger
from app.exceptions import AgentIntegrationError


class HotelSearchAgentClient:
    """Client for Hotel Search Agent integration"""

    def __init__(self) -> None:
        self.base_url = settings.hotel_search_agent_url
        self.timeout = settings.query_timeout

        # Reusable async client (connection pooling)
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
        )

    async def search_hotels(
        self,
        location: str,
        check_in: str,
        check_out: str,
        guests: int,
        preferences: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for hotels"""

        logger.info(f"[HotelAgent] Searching hotels in {location}")

        try:
            response = await self.client.post(
                "/search",
                json={
                    "location": location,
                    "check_in": check_in,
                    "check_out": check_out,
                    "guests": guests,
                    "preferences": preferences or {},
                },
            )

            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            logger.info(f"[HotelAgent] Found {len(results)} hotels")
            return results

        except httpx.TimeoutException:
            logger.error("[HotelAgent] Request timed out")
            raise AgentIntegrationError("Hotel Search Agent timeout")

        except httpx.HTTPStatusError as e:
            logger.error(f"[HotelAgent] HTTP error: {e.response.status_code}")
            raise AgentIntegrationError(
                f"Hotel Search Agent returned {e.response.status_code}"
            )

        except Exception as e:
            logger.error(f"[HotelAgent] Unexpected error: {str(e)}", exc_info=True)
            raise AgentIntegrationError("Hotel Search Agent failed")

    async def get_hotel_details(self, hotel_id: str) -> Dict[str, Any]:
        """Get detailed information for a hotel"""

        logger.info(f"[HotelAgent] Fetching details for hotel {hotel_id}")

        try:
            response = await self.client.get(f"/hotel/{hotel_id}")
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.error(f"[HotelAgent] Failed to fetch hotel details: {str(e)}")
            raise AgentIntegrationError("Failed to fetch hotel details")

    async def get_availability(
        self,
        hotel_id: str,
        check_in: str,
        check_out: str,
    ) -> Dict[str, Any]:
        """Check hotel availability"""

        logger.info(f"[HotelAgent] Checking availability for hotel {hotel_id}")

        try:
            response = await self.client.post(
                "/availability",
                json={
                    "hotel_id": hotel_id,
                    "check_in": check_in,
                    "check_out": check_out,
                },
            )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.error(f"[HotelAgent] Availability check failed: {str(e)}")
            raise AgentIntegrationError("Hotel availability check failed")

    async def close(self) -> None:
        """Close HTTP client"""
        await self.client.aclose()