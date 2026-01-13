# UK WeatherPredict | Predictive Backend Engine

![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Region](https://img.shields.io/badge/region-UK_Only-red.svg)
![API Version](https://img.shields.io/badge/api-v2.1-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 Overview

**UK WeatherPredict** is a specialized high-performance inference engine designed exclusively for meteorological forecasting within the United Kingdom.

Unlike generic global weather APIs, this backend is optimized for the unique microclimates of the British Isles. It accepts geographical coordinates, performs strict region-locking validation, and utilizes a localized historical dataset (calibrated against Met Office patterns) to generate hyper-local weather probabilities.

While the frontend handles user interaction, this backend handles the heavy lifting: **UK-specific coordinate validation, spatial algorithm execution, and predictive forecast generation.**

---

## ✨ Key Features

* **Region-Locked Validation:** Automatically rejects coordinates outside the UK bounding box (approx. 49°N to 61°N) to ensure model accuracy.
* **Microclimate Inference:** Uses a weighted regression model optimized for UK topography (e.g., Highlands vs. Fens).
* **Rain Probability Engine:** Specialized algorithms for high-precision precipitation forecasting, a critical metric for UK users.
* **Type Safety:** Robust handling of input data types to prevent server crashes on malformed requests.

---

## 🏗️ Architecture & Data Flow

The system operates on a linear request-response cycle optimized for accuracy within the UK domain:

1.  **Ingestion (API Gateway):**
    The API endpoint accepts a `POST` request containing geographical coordinates (Latitude/Longitude).

2.  **UK Boundary Guard:**
    The system first verifies if the coordinates fall within the United Kingdom's spatial extents.
    * *Latitude:* 49.00°N - 61.00°N
    * *Longitude:* -8.00°W - 2.00°E
    * *Action:* If outside these bounds, the request is rejected immediately to save processing power.

3.  **Predictive Core:**
    Valid coordinates are mapped against our internal UK climate dataset. The inference algorithm calculates weather stability, precipitation probability, and wind shear based on historical averages for that specific grid reference.

4.  **Response Formatter:**
    The results are serialized into a strict JSON format containing weather-specific metrics.

---