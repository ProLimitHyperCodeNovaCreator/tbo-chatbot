"""Integration with Personalization Agent"""
import httpx
from typing import Dict, Any, Optional, List
from app.config import settings
from app.logger import logger
from app.exceptions import AgentIntegrationError


class PersonalizationAgentClient:
    """Client for Personalization Agent integration"""

    def __init__(self):
        """Initialize personalization agent client"""
        self.base_url = settings.personalization_agent_url

        # Granular timeout config
        self.timeout = httpx.Timeout(
            connect=5.0,
            read=settings.query_timeout,
            write=5.0,
            pool=5.0,
        )

        # Persistent client (connection pooling)
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(
                max_connections=50,
                max_keepalive_connections=20,
            ),
        )

    async def rank_results(
        self,
        user_id: str,
        results: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Rank results based on user personalization
        """
        logger.info(f"Ranking {len(results)} results for user {user_id}")

        try:
            response = await self.client.post(
                f"{self.base_url}/rank",
                json={
                    "user_id": user_id,
                    "results": results,
                    "context": context or {},
                },
            )

            if response.status_code != 200:
                logger.error(
                    f"Personalization agent returned {response.status_code}: {response.text}"
                )
                raise AgentIntegrationError(
                    f"Personalization agent returned {response.status_code}"
                )

            try:
                data = response.json()
            except ValueError:
                raise AgentIntegrationError("Invalid JSON response from personalization agent")

            return data.get("ranked_results", results)

        except httpx.TimeoutException:
            logger.error("Personalization ranking request timed out")
            raise AgentIntegrationError("Personalization service timeout")

        except httpx.RequestError as e:
            logger.error(f"Personalization service request error: {str(e)}")
            raise AgentIntegrationError("Personalization service unavailable") from e

    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user personalization profile"""
        logger.info(f"Fetching profile for user {user_id}")

        try:
            response = await self.client.get(
                f"{self.base_url}/user/{user_id}/profile"
            )

            if response.status_code != 200:
                logger.warning(
                    f"User profile fetch failed with {response.status_code}"
                )
                return {}

            try:
                return response.json()
            except ValueError:
                logger.error("Invalid JSON in user profile response")
                return {}

        except httpx.TimeoutException:
            logger.error("User profile request timed out")
            return {}

        except httpx.RequestError as e:
            logger.error(f"User profile request error: {str(e)}")
            return {}

    async def apply_business_rules(
        self,
        user_id: str,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Apply business rules for user"""
        logger.info(f"Applying business rules for user {user_id}")

        try:
            response = await self.client.post(
                f"{self.base_url}/rules/apply",
                json={"user_id": user_id, "data": data},
            )

            if response.status_code != 200:
                logger.warning(
                    f"Business rules returned {response.status_code}"
                )
                return data

            try:
                parsed = response.json()
            except ValueError:
                logger.error("Invalid JSON in business rules response")
                return data

            return parsed.get("result", data)

        except httpx.TimeoutException:
            logger.error("Business rules request timed out")
            return data

        except httpx.RequestError as e:
            logger.error(f"Business rules request error: {str(e)}")
            return data