"""
Weather service using Open-Meteo API.
Fetches current weather conditions including temperature and precipitation.
"""
import httpx
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import cache, WeatherAPIError, logger


class WeatherService:
    """Service for fetching weather data using Open-Meteo API."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    async def get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get current weather for coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with temperature and precipitation probability
            
        Raises:
            WeatherAPIError: If weather data cannot be fetched
        """
        # Check cache
        cache_key = f"weather_{lat}_{lon}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for weather: ({lat}, {lon})")
            return cached_result
        
        # Make API request
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,precipitation_probability",
            "temperature_unit": "celsius"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.BASE_URL,
                    params=params,
                    timeout=10.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                current = data.get("current", {})
                
                result = {
                    "temperature": current.get("temperature_2m"),
                    "precipitation_probability": current.get("precipitation_probability", 0)
                }
                
                # Cache the result (shorter TTL for weather data)
                cache.set(cache_key, result)
                logger.info(f"Successfully fetched weather for ({lat}, {lon})")
                
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching weather: {str(e)}")
            raise WeatherAPIError(f"Failed to fetch weather data")
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing weather data: {str(e)}")
            raise WeatherAPIError(f"Invalid weather data received")


# Global instance
weather_service = WeatherService()
