import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "model.joblib")

model = joblib.load(MODEL_PATH)

SCALE = 1000

def predict(features: list[float]):
    if len(features) == 0:
        raise ValueError("Feature list is empty")

    x = np.array([features], dtype=float)
    prob = model.predict_proba(x)[0][1]
    label = int(prob > 0.5)

    # ZK circuit integer only → scale
    scaled = [int(f * SCALE) for f in features]

    return label, scaled
