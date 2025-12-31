import numpy as np
import pandas as pd

np.random.seed(42)

N = 500
X = np.random.rand(N, 3)   # 3 features (FIXED)
weights = np.array([2.0, -1.5, 1.0])
bias = -0.2

logits = X @ weights + bias
y = (logits > 0).astype(int)

df = pd.DataFrame(X, columns=["f1", "f2", "f3"])
df["label"] = y

df.to_csv("data/train.csv", index=False)
print("Data generated and saved to data/train.csv")
