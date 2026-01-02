# api/main.py
# uvicorn api.main:app --reload --port 8000
from fastapi import FastAPI, HTTPException
import os
import sys
import shutil
from datetime import datetime
import uvicorn
# ১. রুট ডিরেক্টরি বের করা
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))  # D:\api
BASE_DIR = os.path.dirname(CURRENT_FILE_DIR)  # D:\

sys.path.append(BASE_DIR)

from api.ml.infer import predict
from api.zk.prove import generate_proof
from api.zk.call_contract import verify_onchain, prepare_calldata

app = FastAPI(title="ZK-ML Inference API")
@app.post("/predict")
def predict_endpoint(features: list[float]):
    try:

        # নতুন প্রসেস শুরু করা
        label, scaled = predict(features)
        generate_proof(scaled)
        calldata = prepare_calldata()
        is_valid = verify_onchain(calldata)

        return {
            "prediction": label,
            "proof_generated": True,
            "verifiable_onchain": is_valid
        }

    except Exception as e:
        print(f"Prediction Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)