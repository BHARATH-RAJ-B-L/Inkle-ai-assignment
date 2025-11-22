"""
Custom exception classes and error handling utilities.
Demonstrates troubleshooting and debugging capabilities (JD requirement).
"""
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class TourismAPIError(Exception):
    """Base exception for tourism API errors."""
    pass


class LocationNotFoundError(TourismAPIError):
    """Raised when a location cannot be geocoded."""
    pass


class WeatherAPIError(TourismAPIError):
    """Raised when weather API fails."""
    pass


class PlacesAPIError(TourismAPIError):
    """Raised when places API fails."""
    pass


class RateLimitError(TourismAPIError):
    """Raised when API rate limit is exceeded."""
    pass


def format_error_response(error: Exception) -> Dict[str, Any]:
    """
    Format error into user-friendly response.
    
    Args:
        error: Exception that occurred
        
    Returns:
        Dictionary with error information
    """
    if isinstance(error, LocationNotFoundError):
        return {
            "error": True,
            "message": "I don't know this place exists",
            "type": "location_not_found"
        }
    elif isinstance(error, WeatherAPIError):
        return {
            "error": True,
            "message": "Unable to fetch weather information at the moment",
            "type": "weather_api_error"
        }
    elif isinstance(error, PlacesAPIError):
        return {
            "error": True,
            "message": "Unable to fetch places information at the moment",
            "type": "places_api_error"
        }
    elif isinstance(error, RateLimitError):
        return {
            "error": True,
            "message": "Too many requests. Please try again in a moment.",
            "type": "rate_limit_error"
        }
    else:
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return {
            "error": True,
            "message": "An unexpected error occurred. Please try again.",
            "type": "unknown_error"
        }
