# train_model.py
import os
import joblib
import numpy as np
# NEW IMPORTS
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from src.config import DATA_DIR, MODEL_DIR
from src.architecture import WeatherModelWrapper

def run_training():
    print("--- 3. TRAINING (Gradient Boosting Mode) ---")
    
    # 1. Load Data
    data_path = os.path.join(DATA_DIR, "training_data.joblib")
    if not os.path.exists(data_path):
        print("Error: Run 'prepare_data.py' first.")
        return

    print("Loading prepared data...")
    data = joblib.load(data_path)
    X_dyn = data["X_dyn"]
    X_stat = data["X_stat"]
    y_train = data["y"]
    
    # 2. Flatten Data
    print("Reformatting data...")
    X_dyn_flat = X_dyn.reshape(X_dyn.shape[0], -1)
    X_combined = np.hstack([X_dyn_flat, X_stat])
    
    # 3. Train (THE UPGRADE)
    print("Training Gradient Boosting System...")
    
    # We use HistGradientBoostingRegressor because it's significantly faster 
    # and more accurate for large datasets (>10k samples) than standard GBM.
    gbr = HistGradientBoostingRegressor(
        max_iter=200,          # More iterations = smarter corrections
        learning_rate=0.1,     # How aggressively it corrects errors
        max_depth=10,          # How complex the logic can be
        random_state=42
    )
    
    # Wrap it to handle [Temp, Rain, Wind] all at once
    smart_model = MultiOutputRegressor(gbr)
    smart_model.fit(X_combined, y_train)
    
    # 4. Wrap and Save
    final_model = WeatherModelWrapper(smart_model)
    
    if not os.path.exists(MODEL_DIR): os.makedirs(MODEL_DIR)
    
    save_path = os.path.join(MODEL_DIR, "hybrid_model.joblib")
    joblib.dump(final_model, save_path)
    print(f"Smarter Model saved to {save_path}")

if __name__ == "__main__":
    run_training()