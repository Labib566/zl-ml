import json
import os
from web3 import Web3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert w3.is_connected()

ADDRESS_FILE = os.path.join(BASE_DIR, "api", "zk", "deployed_address.json")
ABI_FILE = os.path.join(
    BASE_DIR,
    "blockchain",
    "artifacts",
    "contracts",
    "ZKMLVerifier.sol",
    "ZKMLVerifier.json"
)

with open(ABI_FILE) as f:
    abi = json.load(f)["abi"]

with open(ADDRESS_FILE) as f:
    CONTRACT_ADDRESS = json.load(f)["zkml"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)


def to_int(x):
    return int(x)


def prepare_calldata():
    with open(os.path.join(BASE_DIR, "zk", "proof.json")) as f:
        proof = json.load(f)

    with open(os.path.join(BASE_DIR, "zk", "public.json")) as f:
        public_inputs = json.load(f)

    # 🔥 EXACT Groth16 mapping
    a = [
        int(proof["pi_a"][0]),
        int(proof["pi_a"][1])
    ]

    b = [
        [
            int(proof["pi_b"][0][0]),
            int(proof["pi_b"][0][1])
        ],
        [
            int(proof["pi_b"][1][0]),
            int(proof["pi_b"][1][1])
        ]
    ]

    c = [
        int(proof["pi_c"][0]),
        int(proof["pi_c"][1])
    ]

    public_inputs = [int(v) for v in public_inputs]

    return a, b, c, public_inputs



def verify_onchain(calldata):
    a, b, c, public_inputs = calldata

    return contract.functions.verifyMLInference(
        a, b, c, public_inputs
    ).call()
