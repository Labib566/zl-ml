import json
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# 🔴 ABSOLUTE PATH (Windows safe) এখানে orginal NODE and SNARKJS path দিতে হবে। 
# পাথ পাওয়ার জন্য terminal a লিখতে হবে(node) where.exe node
# আবার snarkjs এর জন্য (snarkjs) where.exe snarkjs
NODE = r"C:\Program Files\nodejs\node.exe"
SNARKJS = r"C:\Users\nazmu\AppData\Roaming\npm\snarkjs.cmd"

def generate_proof(scaled_input):
    ZK_DIR = os.path.join(BASE_DIR, "zk")

    INPUT_PATH = os.path.join(ZK_DIR, "input.json")
    WITNESS_JS = os.path.join(ZK_DIR, "logreg_js", "generate_witness.js")
    WASM_PATH = os.path.join(ZK_DIR, "logreg_js", "logreg.wasm")
    WITNESS_OUT = os.path.join(ZK_DIR, "witness.wtns")
    ZKEY_PATH = os.path.join(ZK_DIR, "logreg_final.zkey")
    PROOF_OUT = os.path.join(ZK_DIR, "proof.json")
    PUBLIC_OUT = os.path.join(ZK_DIR, "public.json")

    with open(INPUT_PATH, "w") as f:
        json.dump({"x": scaled_input}, f)

    subprocess.run(
        [NODE, WITNESS_JS, WASM_PATH, INPUT_PATH, WITNESS_OUT],
        check=True
    )

    subprocess.run(
        [SNARKJS, "groth16", "prove",
         ZKEY_PATH, WITNESS_OUT, PROOF_OUT, PUBLIC_OUT],
        check=True
    )

    return True
