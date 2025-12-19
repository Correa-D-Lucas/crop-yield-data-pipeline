# utils.py

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2] / "data" / "state_loc.csv"

def csv_to_dict(csv_path: Path | str = BASE_DIR) -> dict:
    """Iterate over Pandas DataFrame rows and return a state centroid dictionary"""
    df = pd.read_csv(csv_path)
    state_centroid = {}

    for _, row in df.iterrows():
        state_centroid[row["state_alpha"]] = {
            "lat":row["latitude"],
            "lon":row["longitude"]
        }
    return state_centroid