/**
 * TripMind AI - Frontend JavaScript
 * Handles API communication and dynamic UI updates
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// Loading messages for multi-agent feedback
const loadingMessages = [
    'AI agents analyzing your destination...',
    'Weather Agent checking forecast...',
    'Places Agent discovering attractions...',
    'Aggregating results from multiple agents...'
];
let loadingMessageIndex = 0;
let loadingMessageInterval = null;

// DOM Elements
const locationInput = document.getElementById('locationInput');
const planButton = document.getElementById('planButton');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const errorCard = document.getElementById('errorCard');
const errorMessage = document.getElementById('errorMessage');
const successResults = document.getElementById('successResults');
const weatherCard = document.getElementById('weatherCard');
const placesCard = document.getElementById('placesCard');
const temperature = document.getElementById('temperature');
const weatherText = document.getElementById('weatherText');
const precipitation = document.getElementById('precipitation');
const placesList = document.getElementById('placesList');

// Example query chips
const exampleChips = document.querySelectorAll('.example-chip');

/**
 * Recent searches management
 */
function getRecentSearches() {
    try {
        return JSON.parse(localStorage.getItem('recentSearches') || '[]');
    } catch {
        return [];
    }
}

function addRecentSearch(location) {
    let recent = getRecentSearches();
    // Remove if already exists
    recent = recent.filter(loc => loc.toLowerCase() !== location.toLowerCase());
    // Add to front
    recent.unshift(location);
    // Keep only last 5
    recent = recent.slice(0, 5);
    localStorage.setItem('recentSearches', JSON.stringify(recent));
    updateRecentSearchesUI();
}

function updateRecentSearchesUI() {
    const recent = getRecentSearches();
    const container = document.querySelector('.example-queries');

    if (recent.length > 0 && !document.querySelector('.recent-label')) {
        const label = document.createElement('span');
        label.className = 'example-label recent-label';
        label.textContent = 'Recent:';
        label.style.marginLeft = '1rem';
        container.appendChild(label);

        recent.forEach(loc => {
            const chip = document.createElement('button');
            chip.className = 'example-chip';
            chip.textContent = `📍 ${loc}`;
            chip.addEventListener('click', () => {
                locationInput.value = loc;
                handlePlanTrip();
            });
            container.appendChild(chip);
        });
    }
}

/**
 * Initialize event listeners
 */
function initializeEventListeners() {
    // Plan button click
    planButton.addEventListener('click', handlePlanTrip);

    // Enter key in input
    locationInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handlePlanTrip();
        }
    });

    // Example chips
    exampleChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const location = chip.getAttribute('data-location');
            locationInput.value = location;
            handlePlanTrip();
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // ESC to clear input and results
        if (e.key === 'Escape') {
            locationInput.value = '';
            resultsSection.classList.add('hidden');
            locationInput.focus();
        }
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            locationInput.focus();
            locationInput.select();
        }
    });
}

/**
 * Main function to handle trip planning
 */
async function handlePlanTrip() {
    const location = locationInput.value.trim();

    // Validate input
    if (!location) {
        showError('Please enter a location');
        return;
    }

    // Show loading state
    showLoading();

    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/plan-trip`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ location })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Hide loading
        hideLoading();

        // Display results
        if (data.success) {
            displayResults(data);
            // Add to recent searches
            addRecentSearch(location);
        } else {
            showError(data.response || 'An error occurred');
        }

    } catch (error) {
        hideLoading();
        console.error('Error:', error);
        showError('Failed to connect to the server. Please make sure the backend is running.');
    }
}

/**
 * Display successful results
 */
function displayResults(data) {
    // Show results section
    resultsSection.classList.remove('hidden');
    errorCard.classList.add('hidden');
    successResults.classList.remove('hidden');

    // Reset cards
    weatherCard.classList.add('hidden');
    placesCard.classList.add('hidden');

    // Display weather if available
    if (data.weather && data.weather.success) {
        displayWeather(data.weather);
    }

    // Display places if available
    if (data.places && data.places.success) {
        displayPlaces(data.places);
    }

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Display weather information
 */
function displayWeather(weatherData) {
    weatherCard.classList.remove('hidden');

    // Set temperature
    const temp = weatherData.temperature;
    temperature.textContent = Math.round(temp);

    // Set weather text
    weatherText.textContent = weatherData.weather_text;

    // Set precipitation
    const precip = weatherData.precipitation_probability;
    precipitation.textContent = `${precip}% rain chance`;
}

/**
 * Display places information
 */
function displayPlaces(placesData) {
    placesCard.classList.remove('hidden');

    // Clear existing list
    placesList.innerHTML = '';

    // Add places
    const places = placesData.places || [];

    if (places.length === 0) {
        placesList.innerHTML = '<li>No attractions found for this location.</li>';
        return;
    }

    places.forEach((place, index) => {
        const li = document.createElement('li');
        li.textContent = place;
        placesList.appendChild(li);
    });
}

/**
 * Show error message
 */
function showError(message) {
    resultsSection.classList.remove('hidden');
    errorCard.classList.remove('hidden');
    successResults.classList.add('hidden');
    errorMessage.textContent = message;

    // Smooth scroll to error
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Show loading state with rotating messages
 */
function showLoading() {
    loadingState.classList.remove('hidden');
    planButton.disabled = true;
    planButton.style.opacity = '0.6';
    resultsSection.classList.add('hidden');

    // Rotate loading messages
    loadingMessageIndex = 0;
    const loadingText = document.querySelector('.loading-text');
    loadingText.textContent = loadingMessages[0];

    loadingMessageInterval = setInterval(() => {
        loadingMessageIndex = (loadingMessageIndex + 1) % loadingMessages.length;
        loadingText.textContent = loadingMessages[loadingMessageIndex];
    }, 1500);
}

/**
 * Hide loading state
 */
function hideLoading() {
    loadingState.classList.add('hidden');
    planButton.disabled = false;
    planButton.style.opacity = '1';

    if (loadingMessageInterval) {
        clearInterval(loadingMessageInterval);
        loadingMessageInterval = null;
    }
}

/**
 * Add smooth entrance animations
 */
function addEntranceAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe cards
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(card);
    });
}

/**
 * Initialize the application
 */
function init() {
    initializeEventListeners();
    updateRecentSearchesUI();
    // addEntranceAnimations(); // Optional: uncomment for extra animations

    // Focus on input
    locationInput.focus();

    console.log('🌍 TripMind AI initialized');
    console.log('💡 Powered by LangGraph Multi-Agent System');
    console.log('⌨️  Keyboard shortcuts: ESC to clear, Ctrl/Cmd+K to focus search');
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
