"""
Places service using Overpass API.
Fetches tourist attractions and points of interest.
"""
import httpx
from typing import List, Dict, Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import cache, PlacesAPIError, logger


class PlacesService:
    """Service for fetching tourist attractions using Overpass API."""
    
    BASE_URL = "https://overpass-api.de/api/interpreter"
    
    async def get_tourist_attractions(
        self, 
        lat: float, 
        lon: float, 
        radius: int = 10000
    ) -> List[str]:
        """
        Get tourist attractions near coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Search radius in meters (default: 10km)
            
        Returns:
            List of up to 5 tourist attraction names
            
        Raises:
            PlacesAPIError: If places data cannot be fetched
        """
        # Check cache
        cache_key = f"places_{lat}_{lon}_{radius}"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for places: ({lat}, {lon})")
            return cached_result
        
        # Build Overpass query for tourist attractions
        query = f"""
        [out:json];
        (
          node["tourism"](around:{radius},{lat},{lon});
          way["tourism"](around:{radius},{lat},{lon});
          node["leisure"="park"](around:{radius},{lat},{lon});
          way["leisure"="park"](around:{radius},{lat},{lon});
          node["historic"](around:{radius},{lat},{lon});
          way["historic"](around:{radius},{lat},{lon});
        );
        out body;
        """
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.BASE_URL,
                    data={"data": query},
                    timeout=15.0
                )
                
                response.raise_for_status()
                data = response.json()
                
                # Extract and filter places
                places = []
                seen_names = set()
                
                for element in data.get("elements", []):
                    tags = element.get("tags", {})
                    name = tags.get("name")
                    
                    if name and name not in seen_names:
                        # Prioritize by tourism type
                        tourism_type = tags.get("tourism", "")
                        leisure_type = tags.get("leisure", "")
                        historic_type = tags.get("historic", "")
                        
                        # Filter for relevant attractions
                        relevant_types = [
                            "attraction", "museum", "gallery", "viewpoint",
                            "zoo", "theme_park", "park", "monument",
                            "palace", "castle", "fort", "memorial"
                        ]
                        
                        if any(t in tourism_type or t in leisure_type or t in historic_type 
                               for t in relevant_types):
                            places.append(name)
                            seen_names.add(name)
                
                # Limit to 5 places
                result = places[:5]
                
                # If we found fewer than 5, try to get any named places
                if len(result) < 5:
                    for element in data.get("elements", []):
                        if len(result) >= 5:
                            break
                        tags = element.get("tags", {})
                        name = tags.get("name")
                        if name and name not in seen_names:
                            result.append(name)
                            seen_names.add(name)
                
                result = result[:5]  # Ensure max 5
                
                # Cache the result
                cache.set(cache_key, result)
                logger.info(f"Successfully fetched {len(result)} places for ({lat}, {lon})")
                
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching places: {str(e)}")
            raise PlacesAPIError("Failed to fetch tourist attractions")
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing places data: {str(e)}")
            raise PlacesAPIError("Invalid places data received")


# Global instance
places_service = PlacesService()
