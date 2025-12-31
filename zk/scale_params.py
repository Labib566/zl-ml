import json

SCALE = 1000

with open("zk/params.json") as f:
    p = json.load(f)

scaled = {
    "weights": [int(w * SCALE) for w in p["weights"]],
    "bias": int(p["bias"] * SCALE),
    "scale": SCALE
}

with open("zk/params_scaled.json", "w") as f:
    json.dump(scaled, f, indent=2)

print(scaled)
