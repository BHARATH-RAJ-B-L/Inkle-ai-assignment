"""
Weather Agent (Child Agent 1)
Fetches current weather information for a location.
"""
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services import geocoding_service, weather_service
from utils import WeatherAPIError, LocationNotFoundError, logger


class WeatherAgent:
    """
    Child Agent 1: Weather Agent
    Responsible for fetching and formatting weather information.
    """
    
    async def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Get weather information for a location.
        
        Args:
            location: Name of the location
            
        Returns:
            Dictionary with weather information and formatted text
        """
        try:
            # Step 1: Geocode the location
            geocode_result = await geocoding_service.geocode(location)
            lat = geocode_result["lat"]
            lon = geocode_result["lon"]
            display_name = geocode_result["display_name"]
            
            # Step 2: Fetch weather data
            weather_data = await weather_service.get_current_weather(lat, lon)
            
            # Step 3: Format the response
            temp = weather_data["temperature"]
            precip = weather_data["precipitation_probability"]
            
            # Extract city name from display name (usually the first part)
            city_name = display_name.split(',')[0]
            
            response_text = (
                f"In {city_name} it's currently {temp}°C "
                f"with a chance of {precip}% to rain."
            )
            
            logger.info(f"Weather agent successfully processed: {location}")
            
            return {
                "success": True,
                "weather_text": response_text,
                "temperature": temp,
                "precipitation_probability": precip,
                "location": city_name
            }
            
        except LocationNotFoundError as e:
            logger.warning(f"Location not found in weather agent: {location}")
            raise
        except WeatherAPIError as e:
            logger.error(f"Weather API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in weather agent: {str(e)}")
            raise WeatherAPIError(f"Failed to fetch weather information")


# Global instance
weather_agent = WeatherAgent()
