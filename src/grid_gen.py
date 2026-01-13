# src/grid_gen.py
import numpy as np

def generate_uk_grid(step_km=25):
    """
    Generates a grid of Lat/Lon points covering the UK.
    """
    # UK Bounding Box (approximate)
    lat_min, lat_max = 50.0, 59.0  # From Cornwall to Orkney
    lon_min, lon_max = -8.0, 1.8   # From N. Ireland to East Anglia
    
    # Conversions (Approx at UK latitude)
    # 1 deg lat ~= 111 km
    # 1 deg lon ~= 65 km (at 55 deg N)
    lat_step = step_km / 111.0
    lon_step = step_km / 65.0
    
    lats = np.arange(lat_min, lat_max, lat_step)
    lons = np.arange(lon_min, lon_max, lon_step)
    
    grid_points = []
    
    # Create the grid
    for lat in lats:
        for lon in lons:
            # (Rough polygon check could go here, but bounding box is fine for now)
            grid_points.append({
                "name": f"Grid_{lat:.2f}_{lon:.2f}",
                "lat": lat,
                "long": lon
            })
            
    return grid_points