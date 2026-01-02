# uvicorn api.main:app --reload --port 8000
from fastapi import FastAPI, HTTPException
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from api.ml.infer import predict
from api.zk.prove import generate_proof
from api.zk.call_contract import verify_onchain, prepare_calldata

app = FastAPI(title="ZK-ML Inference API")

@app.post("/predict")
def predict_endpoint(features: list[float]):
    try:
        # 1️⃣ ML inference
        label, scaled = predict(features)

        # 2️⃣ ZK proof
        generate_proof(scaled)

        # 3️⃣ calldata
        calldata = prepare_calldata()

        # 4️⃣ on-chain verify
        is_valid = verify_onchain(calldata)

        return {
            "prediction": label,
            "proof_generated": True,
            "verifiable_onchain": is_valid
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
