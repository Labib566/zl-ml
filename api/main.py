# api/main.py
# uvicorn api.main:app --reload --port 8000
from fastapi import FastAPI, HTTPException
import os
import sys
import shutil
from datetime import datetime

# ১. রুট ডিরেক্টরি বের করা
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))  # D:\api
BASE_DIR = os.path.dirname(CURRENT_FILE_DIR)  # D:\

sys.path.append(BASE_DIR)

from api.ml.infer import predict
from api.zk.prove import generate_proof
from api.zk.call_contract import verify_onchain, prepare_calldata

app = FastAPI(title="ZK-ML Inference API")

def move_old_files_to_trash():
    """পুরনো proof.json, public.json, witness.wtns ফাইলগুলো trash ফোল্ডারে মুভ করবে"""
    trash_dir = os.path.join(BASE_DIR, "trash")
    os.makedirs(trash_dir, exist_ok=True)

    target_files = [
        "D:\\BLOCKCHAIN_PROJECT\\BLC+ML\\project_00\\chatgpt\\zk\\proof.json", 
        "D:\\BLOCKCHAIN_PROJECT\\BLC+ML\\project_00\\chatgpt\\zk\\public.json", 
        "D:\\BLOCKCHAIN_PROJECT\\BLC+ML\\project_00\\chatgpt\\zk\\witness.wtns"
        ]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # নির্দিষ্ট লোকেশনগুলোতে ফাইল খোঁজা
    search_locations = [
        BASE_DIR,
        os.path.join(BASE_DIR, "api"),
        os.path.join(BASE_DIR, "blockchain")
    ]

    for location in search_locations:
        for file_name in target_files:
            file_path = os.path.join(location, file_name)
            if os.path.exists(file_path):
                new_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
                destination = os.path.join(trash_dir, new_name)
                try:
                    shutil.move(file_path, destination)
                    print(f"--- SUCCESS: {file_name} moved to trash from {location} ---")
                except Exception as e:
                    print(f"--- ERROR moving {file_name}: {e} ---")

@app.post("/predict")
def predict_endpoint(features: list[float]):
    try:
        # প্রথমেই পুরনো ফাইলগুলো trash এ মুভ করা
        move_old_files_to_trash()

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
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)