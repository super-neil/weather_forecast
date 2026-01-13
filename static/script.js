// 1. Initialize Map centered on UK
const map = L.map('map').setView([54.5, -3.5], 6); // UK Center

// 2. Add OpenStreetMap Tiles (The visual map)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let currentMarker = null;

// 3. Handle Map Clicks
map.on('click', async function(e) {
    const lat = parseFloat(e.latlng.lat).toFixed(4);
    const long = parseFloat(e.latlng.lng).toFixed(4);

    // Move Marker
    if (currentMarker) map.removeLayer(currentMarker);
    currentMarker = L.marker([lat, long]).addTo(map);

    // Update UI Loading State
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');
    
    try {
        // 4. Call YOUR Python API
        const response = await fetch(`/predict?lat=${lat}&long=${long}`);
        const data = await response.json();

        // Check for FastAPI error ("detail") OR custom error ("error")
        if (!response.ok || data.detail || data.error) {
            alert("API Error: " + (data.detail || data.error || "Unknown error"));
            return;
        }

        // 5. Update HTML with AI Results
        document.getElementById('temp').innerText = data.forecast.temperature_max_c;
        document.getElementById('rain').innerText = data.forecast.rain_sum_mm;
        document.getElementById('wind').innerText = data.forecast.wind_speed_kmh;
        
        document.getElementById('coords').innerText = `${parseFloat(lat).toFixed(4)}, ${parseFloat(long).toFixed(4)}`;
        document.getElementById('location-name').innerText = `Elevation: ${Math.round(data.location.elevation)}m`;

        // Show Results
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('result').classList.remove('hidden');

    } catch (err) {
        alert("Failed to reach API. Is uvicorn running?");
        console.error(err);
    }
});