import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.read_csv("data/train.csv")

X = df[["f1", "f2", "f3"]].values
y = df["label"].values

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "ml/model.joblib")

print("Model trained & saved")
