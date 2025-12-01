# Flight Tracking Dashboard

*A real-time aviation data visualization tool using the OpenSky Network API*

## Overview

The **Flight Tracking Dashboard** is a real-time aircraft monitoring tool that retrieves live flight data from the OpenSky Network API and visualizes it on an interactive map. The project demonstrates skills in backend development, API integration, data processing, and geospatial visualization—core capabilities for aviation software engineering roles.

This dashboard is part of my larger **Python Data Engineering Portfolio**, with an emphasis on real-world applications in aerospace and flight analytics.

---

## Features

### **Live Aircraft Tracking**

Continuously fetches real-time flight state vectors from OpenSky’s public API.

### Interactive Map Visualization

Displays aircraft across the globe using Plotly Mapbox with hover-inspect details:

* Callsign
* Origin country
* Altitude
* Ground velocity
* Latitude/longitude
* Vertical rate

### Modular Backend Design

The backend is organized into clear components:

* `fetch_opensky.py` — API data retrieval
* `map_helpers.py` — map creation and visualization logic
* `app.py` — Flask server and routing
* `index.html` — UI rendering

### Data Cleaning & Validation

The system handles:

* Missing coordinates
* Incomplete flight state vectors
* Noise and null values in real-time telemetry

### Aviation-Focused Workflow

Mirrors real aviation analytics tasks including:

* ADS-B–style data ingestion
* Fleet-level situational awareness
* Flight monitoring visualization
* Telemetry data transformation

---

## Project Structure

```
flight-tracking-dashboard/
│
├── app.py
├── requirements.txt
├── README.md
│
├── utils/
│   ├── fetch_opensky.py
│   └── map_helpers.py
│
└── templates/
    └── index.html
```

---

## 🔧 Technologies Used

| Category          | Tools                       |
| ----------------- | --------------------------- |
| Language          | Python                      |
| Backend Framework | Flask                       |
| Data Processing   | Pandas                      |
| Visualization     | Plotly + Mapbox             |
| API Source        | OpenSky Network             |
| Geospatial        | Latitude/longitude plotting |

---

## Skills Demonstrated

### **Backend Development**

* Route handling
* Modular Flask application structure
* Server-side rendering

### **API Integration**

* Calling real-time aviation APIs
* Parsing raw JSON telemetry
* Handling network latency and null data

### **Data Engineering**

* Cleaning and validating raw ADS-B–style data
* Converting API responses into analytical structures
* Managing geospatial coordinates

### **Visualization Engineering**

* Interactive map rendering
* Altitude-based color gradients
* Aircraft hover inspection

### **Aviation Analytics**

* Tracking live aircraft states
* Interpreting position, speed, and altitude data
* Building tools aligned with real fleet-monitoring systems

---

## Data Source

This dashboard uses the **OpenSky Network API**, a public aviation telemetry source that provides:

* Aircraft coordinates
* Altitude
* Velocity
* Callsign
* Geospatial state vectors

Endpoint:

```
https://opensky-network.org/api/states/all
```

---

## Why This Project Matters (Aviation Focus)

This project captures essential components of aviation software engineering:

* Real-time data ingestion
* ADS-B-style telemetry processing
* Geospatial visualization
* Building dashboards for operations or analytics teams

---

## Contact

**Amanda Stanley**
Python Developer • Data Engineering 
GitHub: [https://github.com/fullstackattack](https://github.com/fullstackattack)


