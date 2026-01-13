# src/architecture.py
import numpy as np

class WeatherModelWrapper:
    def __init__(self, model):
        self.model = model
        
    def predict(self, inputs):
        # 1. Flatten
        X_dyn = inputs['input_dynamic']
        X_dyn_flat = X_dyn.reshape(X_dyn.shape[0], -1)
        
        # 2. Static
        X_stat = inputs['input_static']
        
        # 3. Combine
        X_combined = np.hstack([X_dyn_flat, X_stat])
        
        # 4. Predict
        preds = self.model.predict(X_combined)
        
        # Handle 1D (single output) or 2D (multi-output)
        if preds.ndim == 1:
            return preds.reshape(-1, 1)
        return preds