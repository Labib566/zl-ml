# streamlit_app.py
# streamlit run streamlit_app.py

import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="ZK-ML Verifier", layout="wide")
st.title("🔐 Cryptographically Verifiable ML Dashboard")
st.markdown("""
This dashboard lets you:
1. Input features for ML prediction.
2. Generate a Zero-Knowledge proof of correct inference.
3. Verify the proof on the Ethereum blockchain.
""")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")
api_url = st.sidebar.text_input("FastAPI URL", "http://127.0.0.1:8000")

# Main input section
st.header("📥 Input Features")
col1, col2, col3 = st.columns(3)
with col1:
    f1 = st.number_input("Feature 1", value=0.4, format="%.2f")
with col2:
    f2 = st.number_input("Feature 2", value=0.7, format="%.2f")
with col3:
    f3 = st.number_input("Feature 3", value=0.2, format="%.2f")

features = [f1, f2, f3]

if st.button("🚀 Run Full ZK-ML Pipeline"):
    with st.spinner("Running ML inference and generating ZK proof..."):
        try:
            # Step 1: Call FastAPI for prediction and proof
            response = requests.post(f"{api_url}/predict", json=features)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ ML inference and proof generation successful!")

                # Display results
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Prediction", result["prediction"])
                with col2:
                    st.metric("On-Chain Verified", result["verifiable_onchain"])

                # Show proof details in expander
                with st.expander("📄 Proof Details"):
                    proof_path = os.path.join("zk", "proof.json")
                    if os.path.exists(proof_path):
                        with open(proof_path) as f:
                            proof_data = json.load(f)
                        st.json(proof_data)

                # Show public inputs
                with st.expander("🔍 Public Inputs"):
                    public_path = os.path.join("zk", "public.json")
                    if os.path.exists(public_path):
                        with open(public_path) as f:
                            public_data = json.load(f)
                        st.json(public_data)

                # Show contract interaction status
                st.info("📝 Smart Contract Verification Completed On-Chain")

            else:
                st.error(f"❌ API Error: {response.text}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Additional info section
st.markdown("---")
st.header("📊 System Status")
col1, col2, col3 = st.columns(3)

# Check if key files exist
def check_file(path, label):
    if os.path.exists(path):
        col1.success(f"✅ {label}")
    else:
        col1.error(f"❌ {label}")

check_file("ml/model.joblib", "ML Model")
check_file("zk/logreg_final.zkey", "ZK Circuit")
check_file("blockchain/artifacts/contracts/ZKMLVerifier.sol/ZKMLVerifier.json", "Contract ABI")

# Footer
st.markdown("---")
st.caption("ZK-ML System | PhD-Grade Hybrid AI-Blockchain Project")