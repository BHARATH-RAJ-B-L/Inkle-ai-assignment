# TripMind AI - Multi-Agent Tourism System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-purple.svg)](https://github.com/langchain-ai/langgraph)

> An intelligent multi-agent tourism planning system powered by LangGraph, demonstrating advanced AI agent orchestration, API integration, and premium UX design.

## 🌐 Live Demo

- **Application:** https://69222661e016f04505379855--tripmindai.netlify.app/
- **Backend API:** https://inkle-ai-assignment.onrender.com
- **API Docs:** https://inkle-ai-assignment.onrender.com/docs
- **GitHub:** https://github.com/BHARATH-RAJ-B-L/Inkle-ai-assignment

## 🎯 Project Overview

TripMind AI is a sophisticated multi-agent system that helps users plan trips by providing:
- 🌤️ **Real-time Weather Information** - Current temperature and precipitation forecasts
- 🏛️ **Tourist Attraction Recommendations** - Up to 5 curated places to visit
- 🤖 **Intelligent Agent Orchestration** - Parent agent coordinates child agents using LangGraph

### Key Features

✅ **Multi-Agent Architecture** - Parent agent orchestrates Weather and Places child agents  
✅ **LangGraph Integration** - StateGraph-based agent flow with conditional routing  
✅ **External API Integration** - Open-Meteo, Nominatim, and Overpass APIs  
✅ **Premium UI/UX** - Glassmorphism effects, smooth animations, responsive design  
✅ **Error Handling** - Graceful handling of invalid locations and API failures  
✅ **Caching & Rate Limiting** - Optimized for data availability and API compliance  

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (HTML/CSS/JS)                  │
│                Premium UI with Glassmorphism                 │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP POST /api/plan-trip
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Parent Agent (Tourism AI)                       │
│              ┌─────────────────────────┐                     │
│              │  LangGraph StateGraph   │                     │
│              │  - Intent Analysis      │                     │
│              │  - Conditional Routing  │                     │
│              │  - Response Aggregation │                     │
│              └─────────────────────────┘                     │
└──────────────────────┬─────────────────┬────────────────────┘
                       │                 │
          ┌────────────┴──────┐  ┌──────┴──────────┐
          ▼                   ▼  ▼                  ▼
    ┌─────────────┐    ┌─────────────┐      ┌──────────────┐
    │   Weather   │    │   Places    │      │   Geocoding  │
    │    Agent    │    │    Agent    │      │   Service    │
    └──────┬──────┘    └──────┬──────┘      └──────┬───────┘
           │                  │                     │
           ▼                  ▼                     ▼
    ┌─────────────┐    ┌─────────────┐      ┌──────────────┐
    │ Open-Meteo  │    │  Overpass   │      │  Nominatim   │
    │     API     │    │     API     │      │     API      │
    └─────────────┘    └─────────────┘      └──────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/BHARATH-RAJ-B-L/Inkle-ai-assignment
   cd Inkle-ai-assignment
   ```

2. **Set up Python virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit .env if needed (default values work fine for testing)
   ```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/api/health`

2. **Start the Frontend**
   
   Open `frontend/index.html` in your browser, or use a simple HTTP server:
   
   ```bash
   # Using Python's built-in server
   cd frontend
   python -m http.server 5500
   ```
   
   Then visit `http://localhost:5500`

   Or use VS Code's Live Server extension.

## 📖 Usage Examples

### Example 1: Plan a Trip (Places Only)
```
Input: "I'm going to go to Bangalore, let's plan my trip"

Output:
In Bangalore these are the places you can go,

- Lalbagh
- Sri Chamarajendra Park
- Bangalore Palace
- Bannerghatta National Park
- Jawaharlal Nehru Planetarium
```

### Example 2: Check Weather
```
Input: "I'm going to go to Bangalore, what is the temperature there"

Output:
In Bangalore it's currently 24°C with a chance of 35% to rain.
```

### Example 3: Combined Query
```
Input: "Weather and places in Bangalore"

Output:
In Bangalore it's currently 24°C with a chance of 35% to rain.
And these are the places you can go,

- Lalbagh
- Sri Chamarajendra Park
- Bangalore Palace
- Bannerghatta National Park
- Jawaharlal Nehru Planetarium
```

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** - Programming language
- **FastAPI** - Modern async web framework
- **LangGraph** - Multi-agent orchestration framework
- **LangChain** - Agent framework and LLM integration
- **Uvicorn** - ASGI server
- **httpx** - Async HTTP client
- **Pydantic** - Data validation

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with glassmorphism
- **JavaScript (ES6+)** - Dynamic interactions
- **Google Fonts** - Inter & Outfit typography

### External APIs
- **Open-Meteo API** - Weather data (no API key required)
- **Nominatim API** - Geocoding (OpenStreetMap)
- **Overpass API** - Tourist attractions (OpenStreetMap)

## 📁 Project Structure

```
Inkle-ai-assignment/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── parent_agent.py      # LangGraph orchestrator
│   │   ├── weather_agent.py     # Child Agent 1
│   │   └── places_agent.py      # Child Agent 2
│   ├── services/
│   │   ├── __init__.py
│   │   ├── geocoding_service.py # Nominatim wrapper
│   │   ├── weather_service.py   # Open-Meteo wrapper
│   │   └── places_service.py    # Overpass wrapper
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── cache.py             # TTL-based cache
│   │   └── error_handler.py     # Error handling
│   ├── tests/                   # Test suite
│   ├── main.py                  # FastAPI application
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
├── frontend/
│   ├── index.html              # Main HTML structure
│   ├── style.css               # Premium CSS styles
│   └── script.js               # Frontend JavaScript
├── README.md
├── SUBMISSION.md
├── DEPLOYMENT.md
└── .gitignore
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Test valid location (e.g., "Bangalore")
- [ ] Test invalid location (e.g., "XYZ123")
- [ ] Test weather-only query (e.g., "weather in Paris")
- [ ] Test places-only query (e.g., "places in Tokyo")
- [ ] Test combined query
- [ ] Test responsive design on mobile
- [ ] Verify error messages are user-friendly
- [ ] Check loading states appear correctly

### API Testing

You can test the API directly using the interactive docs:
```
https://inkle-ai-assignment.onrender.com/docs
```

Or using curl:
```bash
curl -X POST "https://inkle-ai-assignment.onrender.com/api/plan-trip" \
  -H "Content-Type: application/json" \
  -d '{"location": "Bangalore"}'
```

## 🔧 Configuration

Environment variables in `.env`:

```bash
# API Configuration
NOMINATIM_USER_AGENT=tripmind-ai
NOMINATIM_EMAIL=your-email@example.com

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration
FRONTEND_URL=http://localhost:5500

# Cache Configuration
CACHE_TTL_SECONDS=3600
```

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.9+ is installed: `python --version`
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

### Frontend can't connect to backend
- Verify backend is running on `http://localhost:8000`
- Check CORS settings in `backend/main.py`
- Check browser console for errors

### No places found for a location
- Some locations may have limited tourist data in OpenStreetMap
- Try major cities like "Paris", "Tokyo", "New York"

### Rate limit errors
- Nominatim has a 1 req/sec limit
- The app includes rate limiting and caching
- Wait a few seconds between requests

## 📝 License

This project was created as a demonstration of multi-agent AI systems.

## 👨‍💻 Author

**Bharath Raj B L**  
GitHub: https://github.com/BHARATH-RAJ-B-L

---

**Note**: This project demonstrates:
- ✅ Multi-agent AI systems
- ✅ LangGraph/LangChain frameworks
- ✅ API integration and orchestration
- ✅ Modern web development
- ✅ Error handling and debugging
- ✅ Premium UI/UX design

Built with ❤️ using Python, FastAPI, and LangGraph
