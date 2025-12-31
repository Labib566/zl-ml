import joblib
import numpy as np

model = joblib.load("ml/model.joblib")

x = np.array([[0.4, 0.7, 0.2]])
pred = model.predict_proba(x)

print("Probability:", pred)
print("Class:", int(pred[0][1] > 0.5))
