# src/preprocessing.py
import numpy as np
import pandas as pd
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
from .config import FEATURES_DYNAMIC, FEATURES_STATIC, MODEL_DIR, SEQ_LENGTH

class WeatherPreprocessor:
    def __init__(self):
        self.scaler_dyn = MinMaxScaler()
        self.scaler_stat = MinMaxScaler()
        self.is_fitted = False

    def add_seasonality(self, df):
        # 1. Cyclical Date
        day = df['date'].dt.dayofyear
        df['day_sin'] = np.sin(2 * np.pi * day / 365.0)
        df['day_cos'] = np.cos(2 * np.pi * day / 365.0)
        return df

    def add_derived_features(self, df):
        # Ensure we don't overwrite the original dataframe
        df = df.copy()
        
        # 3-Day Rolling Average for Temp (Trend detection)
        df['temp_roll_3'] = df['temp'].rolling(window=3).mean()
        
        # 3-Day Rolling Average for Rain (Storm detection)
        df['rain_roll_3'] = df['rain'].rolling(window=3).mean()

        # "Today's Pressure" minus "Yesterday's Pressure"
        # Negative value = Pressure dropping (Storm approaching)
        # Positive value = Pressure rising (Clearing up)
        df['pressure_trend'] = df['pressure'].diff()
        
        # Rolling creates NaNs for the first 2 days. Fill them.
        # 'bfill' = Backwards Fill (use day 3's data for day 1 & 2)
        #df = df.bfill()
        df = df.ffill().bfill().fillna(0)
        
        return df

    def fit(self, df):
        # Process features BEFORE fitting the scaler
        df = self.add_seasonality(df)
        df = self.add_derived_features(df)
        
        self.scaler_dyn.fit(df[FEATURES_DYNAMIC])
        self.scaler_stat.fit(df[FEATURES_STATIC])
        self.is_fitted = True

    def save(self):
        if not os.path.exists(MODEL_DIR): os.makedirs(MODEL_DIR)
        joblib.dump(self.scaler_dyn, os.path.join(MODEL_DIR, "scaler_dyn.save"))
        joblib.dump(self.scaler_stat, os.path.join(MODEL_DIR, "scaler_stat.save"))

    def load(self):
        self.scaler_dyn = joblib.load(os.path.join(MODEL_DIR, "scaler_dyn.save"))
        self.scaler_stat = joblib.load(os.path.join(MODEL_DIR, "scaler_stat.save"))
        self.is_fitted = True

    def create_sequences(self, df, is_training=True):
        # Apply math
        df = self.add_seasonality(df)
        df = self.add_derived_features(df) # <--- Apply Memory Here
        
        # Scale
        # Now FEATURES_DYNAMIC includes the 2 new columns, so this works automatically
        dyn_scaled = self.scaler_dyn.transform(df[FEATURES_DYNAMIC])
        stat_scaled = self.scaler_stat.transform(df[FEATURES_STATIC])
        
        if not is_training:
            return (
                dyn_scaled[-SEQ_LENGTH:].reshape(1, SEQ_LENGTH, len(FEATURES_DYNAMIC)),
                stat_scaled[-1].reshape(1, len(FEATURES_STATIC))
            )

        # Targets: Temp, Rain, Wind
        target_cols = ['temp', 'rain', 'wind']
        targets = df[target_cols].shift(-1).values 
        
        X_dyn, X_stat, y = [], [], []
        
        for i in range(len(dyn_scaled) - SEQ_LENGTH):
            if np.isnan(targets[i + SEQ_LENGTH]).any(): continue
            
            X_dyn.append(dyn_scaled[i:i+SEQ_LENGTH])
            X_stat.append(stat_scaled[i])
            y.append(targets[i+SEQ_LENGTH])
            
        return np.array(X_dyn), np.array(X_stat), np.array(y)