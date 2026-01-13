# 🧠 GeoPredictor Backend Engine

![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![API Version](https://img.shields.io/badge/api-v1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 Overview

**GeoPredictor Backend** is the high-performance inference engine powering the GeoCoordinate project. Unlike standard geospatial tools, this system acts as an intelligent layer that accepts raw geographical input, performs robust data sanitization, and utilizes historical datasets to generate predictive insights.

While the frontend serves as the entry point, this backend handles the critical logic: **input validation, spatial algorithm execution, and JSON response generation.**

---

## ✨ Key Features

* **Robust Input Sanitization:** Automatically detects and converts data types (handling String/Float mismatches) to prevent runtime errors.
* **Predictive Inference:** Uses historical spatial data to calculate probabilities based on location.
* **High-Speed API:** Lightweight RESTful architecture designed for low-latency responses.
* **Error Handling:** Graceful degradation and detailed error messaging for malformed coordinates.

---

## 🏗️ Architecture & Data Flow

The system operates on a linear request-response cycle optimized for accuracy:

1.  **Ingestion (API Gateway):**
    The API endpoint accepts a `POST` request containing geographical coordinates (Latitude/Longitude).

2.  **Validation Guard:**
    The system inspects incoming variables to ensure they are valid numbers. It handles type conversion (e.g., parsing strings to floats) to prevent `TypeError` crashes before they reach the core logic.

3.  **Predictive Core:**
    Once validated, coordinates are mapped against internal datasets. The inference algorithm determines the predictive outcome based on spatial density and historical trends.

4.  **Response Formatter:**
    The results are serialized into a strict JSON format, ready for consumption by the client.

---

## 🔌 API Documentation

### Get Prediction
Returns a predictive analysis based on the provided location.

* **URL:** `/api/v1/predict`
* **Method:** `POST`
* **Content-Type:** `application/json`

#### Request Payload
```json
{
  "latitude": "40.7128", 
  "longitude": -74.0060,
  "timestamp": "2023-10-27T10:00:00Z"
}
```
Success Response (200 OK)

```json
{
  "status": "success",
  "data": {
    "prediction": "High Probability",
    "confidence_score": 0.94,
    "input_summary": {
      "lat": 40.71,
      "lng": -74.01
    }
  }
}
```

Error Response (400 Bad Request)

```json
{
  "status": "error",
  "message": "Invalid coordinate format. 'lat' must be parsable as a number."
}
```

## 📄 License
Distributed under the MIT License.