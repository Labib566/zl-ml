import joblib
import json

model = joblib.load("ml/model.joblib")

params = {
    "weights": model.coef_[0].tolist(),
    "bias": float(model.intercept_[0])
}

with open("zk/params.json", "w") as f:
    json.dump(params, f, indent=2)

print(params)
