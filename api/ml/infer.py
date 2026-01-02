import joblib
import numpy as np
import os

# ১. পাথ সেটআপ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "model.joblib")

# মডেল লোড করা (এটি মূলত ফিচারের সংখ্যা বা অন্য তথ্যের জন্য রাখা হয়েছে)
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

def predict(features: list[float]):
    if len(features) == 0:
        raise ValueError("Feature list is empty")

    # ২. আপনার logreg.circom ফাইলের সাথে মিল রেখে লজিক সেট করা
    # সার্কিটে আপনি এই মানগুলো ব্যবহার করেছেন: w = [2010, -1490, 980], b = -210
    W = np.array([6247, -4899, 2851])
    B = 20
    SCALE = 1000

    # ৩. ইনপুট স্কেলিং (Decimal to Integer)
    scaled = [int(f * SCALE) for f in features]
    scaled_np = np.array(scaled)

    # ৪. সার্কিটের গাণিতিক সমীকরণ: z = x0*w0 + x1*w1 + x2*w2 + b
    z = np.dot(scaled_np, W) + B

    # ৫. লেবেল নির্ধারণ (সার্কিটের GreaterThan লজিক অনুযায়ী)
    # যদি z > 0 হয় তবে ১, নতুবা ০
    label = 1 if z > 0 else 0

    return label, scaled