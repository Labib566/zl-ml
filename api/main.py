from fastapi import FastAPI, HTTPException
import os
import sys
import shutil
from datetime import datetime

# ১. সরাসরি বর্তমান ফাইলের লোকেশন থেকে রুট খুঁজে বের করা
# এই লাইনটি নিশ্চিত করবে যে আমরা সবসময় সঠিক ফোল্ডার থেকে ফাইল খুঁজছি
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__)) # D:\api
BASE_DIR = os.path.dirname(CURRENT_FILE_DIR) # D:\

sys.path.append(BASE_DIR)

from api.ml.infer import predict
from api.zk.prove import generate_proof
from api.zk.call_contract import verify_onchain, prepare_calldata

app = FastAPI(title="ZK-ML Inference API")

def move_old_files_to_trash():
    # ২. ট্র্যাশ ফোল্ডারটি রুট ডিরেক্টরিতে তৈরি করা (D:\trash)
    trash_dir = os.path.join(BASE_DIR, "trash")
    if not os.path.exists(trash_dir):
        os.makedirs(trash_dir)

    target_files = ["proof.json", "public.json", "witness.wtns"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ৩. সম্ভাব্য সব জায়গায় ফাইলগুলো খোঁজা (রুট, এপিআই ফোল্ডার, ব্লকচেইন ফোল্ডার)
    search_locations = [
        BASE_DIR,
        os.getcwd(), # বর্তমানে টার্মিনাল যে ফোল্ডারে আছে
        os.path.join(BASE_DIR, "blockchain")
    ]

    for location in search_locations:
        for file_name in target_files:
            file_path = os.path.join(location, file_name)
            
            if os.path.exists(file_path):
                # নতুন নাম এবং গন্তব্য ঠিক করা
                new_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
                destination = os.path.join(trash_dir, new_name)
                
                try:
                    # ফাইলটি মুভ করা (কপি নয়, সরাসরি সরিয়ে ফেলা)
                    shutil.move(file_path, destination)
                    print(f"--- SUCCESS: {file_name} moved to trash from {location} ---")
                except Exception as e:
                    print(f"--- ERROR moving {file_name}: {e} ---")

@app.post("/predict")
def predict_endpoint(features: list[float]):
    try:
        # ৪. প্রথমেই ক্লিনিং ফাংশন কল করা
        move_old_files_to_trash()

        # ৫. বাকি প্রসেসগুলো শুরু করা
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