# main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import joblib
import os
import datetime

from src.preprocessing import WeatherPreprocessor
from src.ingestion import fetch_weather_data
from src.config import MODEL_DIR
# Import the wrapper so joblib can find the class definition
from src.architecture import WeatherModelWrapper

system = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("--- SYSTEM STARTUP ---")
        
        # Load Model
        model_path = os.path.join(MODEL_DIR, "hybrid_model.joblib")
        print(f"Loading Model from {model_path}...")
        
        system['model'] = joblib.load(model_path)
        
        # Load Preprocessor
        print("Loading Preprocessor...")
        processor = WeatherPreprocessor()
        processor.load()
        system['processor'] = processor
            
        print("--- SYSTEM READY ---")
        yield
        
    except Exception as e:
        print(f"CRITICAL STARTUP ERROR: {e}")
        yield
    finally:
        system.clear()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Read the index.html file and send it to the browser
    with open("static/index.html") as f:
        return f.read()

@app.get("/predict")
async def get_forecast(lat: float, long: float):
    if 'model' not in system:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    try:
        # 1. Fetch
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=30)
        df = fetch_weather_data(lat, long, str(start_date), str(today))
        
        if len(df) < 14:
            raise HTTPException(status_code=400, detail="Insufficient data.")

        # 2. Process
        processor = system['processor']
        X_dyn, X_stat = processor.create_sequences(df, is_training=False)
        
        # 3. Predict
        model = system['model']
        # The model returns shape (1, 3) -> [[Temp, Rain, Wind]]
        predictions = model.predict({'input_dynamic': X_dyn, 'input_static': X_stat})
        
        # 4. Unpack Results
        # We grab the first row (index 0) and split it into variables
        pred_temp = predictions[0][0]
        pred_rain = predictions[0][1]
        pred_wind = predictions[0][2]
        
        # Logic: If rain is negative (impossible but math can do it), set to 0
        if pred_rain < 0: pred_rain = 0.0
        
        return {
            "location": {
                "lat": lat, 
                "long": long, 
                "elevation": float(df['elevation'].iloc[0])
            },
            "forecast": {
                "date": str(today + datetime.timedelta(days=1)),
                "temperature_max_c": round(float(pred_temp), 2),
                "rain_sum_mm": round(float(pred_rain), 2),
                "wind_speed_kmh": round(float(pred_wind), 2),
                "description": "Hybrid Multi-Output RF"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))