import joblib
import numpy as np
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

model = joblib.load("ml/model.joblib")

initial_type = [("input", FloatTensorType([1, 3]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)

with open("zk/model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

print("ONNX model exported")
