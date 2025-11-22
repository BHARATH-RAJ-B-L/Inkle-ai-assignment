"""
Tests for Multi-Agent Tourism System
Demonstrates testing skills and quality assurance.
"""
import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agents.weather_agent import weather_agent
from agents.places_agent import places_agent
from agents.parent_agent import parent_agent


class TestWeatherAgent:
    """Tests for Weather Agent."""
    
    @pytest.mark.asyncio
    async def test_weather_agent_valid_location(self):
        """Test weather agent with valid location."""
        result = await weather_agent.get_weather("London")
        
        assert result["success"]  == True
        assert "temperature" in result
        assert "precipitation" in result
        assert isinstance(result["temperature"], (int, float))
        
    @pytest.mark.asyncio
    async def test_weather_agent_invalid_location(self):
        """Test weather agent with invalid location."""
        result = await weather_agent.get_weather("INVALIDXYZ123")
        
        assert result["success"] == False
        assert "error" in result


class TestPlacesAgent:
    """Tests for Places Agent."""
    
    @pytest.mark.asyncio
    async def test_places_agent_valid_location(self):
        """Test places agent with valid location."""
        result = await places_agent.get_attractions("Paris")
        
        assert result["success"] == True
        assert "places" in result
        assert isinstance(result["places"], list)
        assert len(result["places"]) <= 5
        
    @pytest.mark.asyncio
    async def test_places_agent_invalid_location(self):
        """Test places agent with invalid location."""
        result = await places_agent.get_attractions("INVALIDXYZ123")
        
        assert result["success"] == False


class TestParentAgent:
    """Tests for Parent Agent (LangGraph Orchestrator)."""
    
    @pytest.mark.asyncio
    async def test_parent_agent_weather_query(self):
        """Test parent agent with weather-focused query."""
        result = await parent_agent.process_query("What's the weather in Tokyo?")
        
        assert result["success"] == True
        assert "weather" in result["response"].lower()
        
    @pytest.mark.asyncio
    async def test_parent_agent_places_query(self):
        """Test parent agent with places-focused query."""
        result = await parent_agent.process_query("What places can I visit in Rome?")
        
        assert result["success"] == True
        assert result.get("places") is not None or "place" in result["response"].lower()
        
    @pytest.mark.asyncio
    async def test_parent_agent_combined_query(self):
        """Test parent agent with combined query."""
        result = await parent_agent.process_query("Weather and places in Barcelona")
        
        assert result["success"] == True
        # Should have both weather and places data
        
    @pytest.mark.asyncio
    async def test_parent_agent_invalid_location(self):
        """Test parent agent with invalid location."""
        result = await parent_agent.process_query("INVALIDXYZ123")
        
        # Should handle gracefully
        assert result["success"] == False
        assert "not found" in result["response"].lower() or "don't know" in result["response"].lower()


class TestAPIEndpoints:
    """Tests for FastAPI endpoints."""
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/api/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
    def test_stats_endpoint(self):
        """Test statistics endpoint."""
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/api/stats")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "uptime_seconds" in data
        assert "total_requests" in data
        
    def test_plan_trip_valid(self):
        """Test plan-trip endpoint with valid location."""
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.post("/api/plan-trip", json={"location": "Singapore"})
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "response" in data
        
    def test_plan_trip_validation(self):
        """Test plan-trip endpoint validation."""
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Empty location
        response = client.post("/api/plan-trip", json={"location": ""})
        assert response.status_code == 422  # Validation error
        
        # XSS attempt
        response = client.post("/api/plan-trip", json={"location": "<script>alert('xss')</script>"})
        assert response.status_code == 422  # Validation error
        
    def test_rate_limiting(self):
        """Test rate limiting functionality."""
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Make multiple requests
        for i in range(12):
            response = client.post("/api/plan-trip", json={"location": f"Test{i}"})
            if i < 10:
                # Should succeed
                assert response.status_code == 200
            else:
                # Should be rate limited
                assert response.status_code == 429


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
