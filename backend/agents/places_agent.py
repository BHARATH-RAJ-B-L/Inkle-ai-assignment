"""
Places Agent (Child Agent 2)
Fetches tourist attraction recommendations for a location.
"""
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services import geocoding_service, places_service
from utils import PlacesAPIError, LocationNotFoundError, logger


class PlacesAgent:
    """
    Child Agent 2: Places Agent
    Responsible for fetching and formatting tourist attraction information.
    """
    
    async def get_places(self, location: str) -> Dict[str, Any]:
        """
        Get tourist attractions for a location.
        
        Args:
            location: Name of the location
            
        Returns:
            Dictionary with places list and formatted text
        """
        try:
            # Step 1: Geocode the location
            geocode_result = await geocoding_service.geocode(location)
            lat = geocode_result["lat"]
            lon = geocode_result["lon"]
            display_name = geocode_result["display_name"]
            
            # Step 2: Fetch tourist attractions
            places = await places_service.get_tourist_attractions(lat, lon)
            
            # Step 3: Format the response
            city_name = display_name.split(',')[0]
            
            if not places:
                response_text = f"I couldn't find tourist attractions in {city_name}."
                logger.warning(f"No places found for: {location}")
            else:
                response_text = f"In {city_name} these are the places you can go,\n\n"
                response_text += "\n".join([f"- {place}" for place in places])
            
            logger.info(f"Places agent successfully processed: {location}, found {len(places)} places")
            
            return {
                "success": True,
                "places_text": response_text,
                "places": places,
                "location": city_name
            }
            
        except LocationNotFoundError as e:
            logger.warning(f"Location not found in places agent: {location}")
            raise
        except PlacesAPIError as e:
            logger.error(f"Places API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in places agent: {str(e)}")
            raise PlacesAPIError(f"Failed to fetch places information")


# Global instance
places_agent = PlacesAgent()
