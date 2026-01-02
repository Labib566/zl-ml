import joblib
model = joblib.load("ml/model.joblib")

# স্কেলিং ফ্যাক্টর ১০০০ দিয়ে গুণ করে পূর্ণসংখ্যায় রূপান্তর
weights = model.coef_[0] * 1000
bias = model.intercept_[0] * 1000

print(f"Weights: {[int(w) for w in weights]}")
print(f"Bias: {int(bias)}")