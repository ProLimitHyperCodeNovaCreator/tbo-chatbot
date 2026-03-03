"""Integration with Amadeus Agent (TBO)"""
import httpx
from typing import Dict, Any, List, Optional
from app.config import settings
from app.logger import logger
from app.exceptions import AgentIntegrationError


class AmadeusAgentClient:
    """Client for Amadeus/TBO Agent integration"""

    def __init__(self):
        """Initialize Amadeus agent client"""
        self.base_url = settings.amadeus_agent_url

        # Structured timeout
        self.timeout = httpx.Timeout(
            connect=5.0,
            read=settings.query_timeout,
            write=5.0,
            pool=5.0,
        )

        # Persistent client with connection pooling
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=30,
            ),
        )

    async def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        passengers: int = 1,
        preferences: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for flights"""

        logger.info(f"Searching flights from {origin} to {destination}")

        try:
            response = await self.client.post(
                f"{self.base_url}/search",
                json={
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "return_date": return_date,
                    "passengers": passengers,
                    "preferences": preferences or {},
                },
            )

            if response.status_code != 200:
                logger.error(
                    f"Amadeus agent returned {response.status_code}: {response.text}"
                )
                raise AgentIntegrationError(
                    f"Amadeus agent returned {response.status_code}"
                )

            try:
                data = response.json()
            except ValueError:
                raise AgentIntegrationError(
                    "Invalid JSON response from Amadeus agent"
                )

            return data.get("results", [])

        except httpx.TimeoutException:
            logger.error("Flight search request timed out")
            raise AgentIntegrationError("Flight service timeout")

        except httpx.RequestError as e:
            logger.error(f"Flight service request error: {str(e)}")
            raise AgentIntegrationError("Flight service unavailable") from e

    async def get_flight_details(self, flight_id: str) -> Dict[str, Any]:
        """Get detailed information for a flight"""

        logger.info(f"Fetching details for flight {flight_id}")

        try:
            response = await self.client.get(
                f"{self.base_url}/flight/{flight_id}"
            )

            if response.status_code != 200:
                logger.warning(
                    f"Flight details returned {response.status_code}"
                )
                return {}

            try:
                return response.json()
            except ValueError:
                logger.error("Invalid JSON in flight details response")
                return {}

        except httpx.TimeoutException:
            logger.error("Flight details request timed out")
            return {}

        except httpx.RequestError as e:
            logger.error(f"Flight details request error: {str(e)}")
            return {}

    async def get_travel_packages(
        self,
        origin: str,
        destination: str,
        dates: Dict[str, str],
    ) -> List[Dict[str, Any]]:
        """Get travel packages (flight + hotel combinations)"""

        logger.info(f"Fetching packages from {origin} to {destination}")

        try:
            response = await self.client.post(
                f"{self.base_url}/packages",
                json={
                    "origin": origin,
                    "destination": destination,
                    "dates": dates,
                },
            )

            if response.status_code != 200:
                logger.error(
                    f"Travel packages returned {response.status_code}"
                )
                raise AgentIntegrationError(
                    f"Travel packages error {response.status_code}"
                )

            try:
                data = response.json()
            except ValueError:
                raise AgentIntegrationError(
                    "Invalid JSON in travel packages response"
                )

            return data.get("packages", [])

        except httpx.TimeoutException:
            logger.error("Travel packages request timed out")
            raise AgentIntegrationError("Package service timeout")

        except httpx.RequestError as e:
            logger.error(f"Travel packages request error: {str(e)}")
            raise AgentIntegrationError("Package service unavailable") from e

    async def verify_availability(
        self,
        flight_id: str,
        passengers: int,
    ) -> Dict[str, Any]:
        """Verify flight availability"""

        logger.info(f"Verifying availability for flight {flight_id}")

        try:
            response = await self.client.post(
                f"{self.base_url}/verify",
                json={
                    "flight_id": flight_id,
                    "passengers": passengers,
                },
            )

            if response.status_code != 200:
                logger.warning(
                    f"Availability check returned {response.status_code}"
                )
                return {"available": False}

            try:
                return response.json()
            except ValueError:
                logger.error("Invalid JSON in availability response")
                return {"available": False}

        except httpx.TimeoutException:
            logger.error("Availability verification timed out")
            return {"available": False}

        except httpx.RequestError as e:
            logger.error(f"Availability request error: {str(e)}")
            return {"available": False}