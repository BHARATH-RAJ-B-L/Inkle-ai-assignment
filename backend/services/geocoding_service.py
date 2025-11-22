"""
Geocoding service using Nominatim API.
Converts place names to coordinates with proper rate limiting and caching.
"""
import httpx
import asyncio
from typing import Optional, Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import cache, LocationNotFoundError, RateLimitError, logger
import os
from dotenv import load_dotenv

load_dotenv()

# Import settings for retry configuration
try:
    from settings import settings
    MAX_RETRIES = settings.max_retries
    RETRY_DELAY = settings.retry_delay
except ImportError:
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0


class GeocodingService:
    """Service for geocoding location names using Nominatim API."""
    
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    def __init__(self):
        self.user_agent = os.getenv("NOMINATIM_USER_AGENT", "inkle-tourism-app")
        self.email = os.getenv("NOMINATIM_EMAIL", "demo@example.com")
        self.last_request_time = 0
        self.rate_limit_delay = 1.0  # Nominatim requires 1 second between requests
    
    async def _respect_rate_limit(self):
        """Ensure we don't exceed Nominatim's rate limit (1 req/sec)."""
        current_time = asyncio.get_event_loop().time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = asyncio.get_event_loop().time()
    
    async def geocode(self, location: str) -> Dict[str, Any]:
        """
        Convert location name to coordinates.
        
        Args:
            location: Name of the place to geocode
            
        Returns:
            Dictionary with lat, lon, and display_name
            
        Raises:
            LocationNotFoundError: If location cannot be found
            RateLimitError: If rate limit is exceeded
        """
        # Check cache first
        cache_key = f"geocode_{location.lower()}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for geocoding: {location}")
            return cached_result
        
        # Respect rate limit
        await self._respect_rate_limit()
        
        # Prepare request parameters
        params = {
            "q": location,
            "format": "json",
            "limit": 1,
            "email": self.email
        }
        
        headers = {
            "User-Agent": self.user_agent
        }
        
        # Make API request with retry logic
        for attempt in range(MAX_RETRIES):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        self.BASE_URL,
                        params=params,
                        headers=headers,
                        timeout=10.0
                    )
                    
                    if response.status_code == 429:
                        logger.warning("Rate limit exceeded for Nominatim API")
                        if attempt < MAX_RETRIES - 1:
                            await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                            continue
                        raise RateLimitError("Geocoding rate limit exceeded")
                    
                    response.raise_for_status()
                    data = response.json()
                    
                    if not data:
                        logger.warning(f"Location not found: {location}")
                        raise LocationNotFoundError(f"Location '{location}' not found")
                    
                    result = {
                        "lat": float(data[0]["lat"]),
                        "lon": float(data[0]["lon"]),
                        "display_name": data[0]["display_name"]
                    }
                    
                    # Cache the result
                    cache.set(cache_key, result)
                    logger.info(f"Successfully geocoded: {location}")
                    
                    return result
                    
            except httpx.HTTPError as e:
                if attempt < MAX_RETRIES - 1:
                    logger.warning(f"HTTP error during geocoding (attempt {attempt + 1}/{MAX_RETRIES}): {str(e)}")
                    await asyncio.sleep(RETRY_DELAY * (attempt + 1))
                    continue
                logger.error(f"HTTP error during geocoding: {str(e)}")
                raise LocationNotFoundError(f"Failed to geocode location: {location}")


# Global instance
geocoding_service = GeocodingService()
