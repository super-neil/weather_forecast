# src/config.py
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Model Settings
SEQ_LENGTH = 14

FEATURES_DYNAMIC = [
    'temp', 'rain', 'wind', 'humid', 
    'pressure', 'cloud',
    'day_sin', 'day_cos', 
    'temp_roll_3', 'rain_roll_3',
    'pressure_trend'
]

FEATURES_STATIC = ['lat', 'long', 'elevation']

# Training List
TRAINING_LOCATIONS = [
    {"name": "London", "lat": 51.5074, "long": -0.1278},
    {"name": "Ben Nevis", "lat": 56.7969, "long": -5.0036},
    {"name": "Cornwall", "lat": 50.2660, "long": -5.0527},
    {"name": "Manchester", "lat": 53.4808, "long": -2.2426},
    {"name": "Snowdon", "lat": 53.0685, "long": -4.0763}
]