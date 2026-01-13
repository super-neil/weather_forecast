# prepare_data.py
import pandas as pd
import numpy as np
import os
import joblib
import time
from tqdm import tqdm # Progress bar
from src.config import DATA_DIR
from src.ingestion import fetch_weather_data
from src.preprocessing import WeatherPreprocessor
from src.grid_gen import generate_uk_grid 

def run_etl_pipeline():
    print("--- 1. GENERATING GRID ---")
    # Generate ~400 points
    locations = generate_uk_grid(step_km=25)
    print(f"Generated {len(locations)} monitoring points across the UK.")
    
    print("--- 2. INGESTION (Network Phase) ---")
    data_frames = []
    
    # Use TQDM to show a progress bar
    for loc in tqdm(locations, desc="Fetching Weather History"):
        try:
            # We fetch 3 years of data for each point
            df = fetch_weather_data(loc['lat'], loc['long'], "2021-01-01", "2024-01-01")
            
            # Simple check: If elevation is 0 (ocean), we might want to skip?
            # Actually, keeping ocean points helps predict coastal weather!
            data_frames.append(df)
            
            # Be polite to the API (Open-Meteo limit is high, but good practice)
            time.sleep(0.1) 
            
        except Exception as e:
            # If one point fails, don't crash the whole script
            # print(f"Skipped {loc['name']}: {e}")
            pass
    
    if not data_frames:
        print("CRITICAL: No data fetched.")
        return

    print(f"Successfully collected {len(data_frames)} locations.")
    full_df = pd.concat(data_frames)
    
    print("--- 3. PREPROCESSING (Math Phase) ---")
    processor = WeatherPreprocessor()
    processor.fit(full_df)
    processor.save()
    print("Scalers saved.")

    X_dyn_list, X_stat_list, y_list = [], [], []
    
    for df in tqdm(data_frames, desc="Building Sequences"):
        Xd, Xs, y = processor.create_sequences(df)
        X_dyn_list.append(Xd)
        X_stat_list.append(Xs)
        y_list.append(y)
        
    X_dyn_train = np.concatenate(X_dyn_list)
    X_stat_train = np.concatenate(X_stat_list)
    y_train = np.concatenate(y_list)
    
    # Save
    if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)
    save_path = os.path.join(DATA_DIR, "training_data.joblib")
    
    joblib.dump({
        "X_dyn": X_dyn_train,
        "X_stat": X_stat_train,
        "y": y_train
    }, save_path)
    
    print(f"Dataset compiled: {len(y_train)} total training samples.")
    print(f"Data saved to {save_path}")

if __name__ == "__main__":
    run_etl_pipeline()