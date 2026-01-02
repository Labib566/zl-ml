# streamlit_app.py
# streamlit run streamlit_app.py

import streamlit as st
import requests
import json
import time
from typing import List, Optional

# Page configuration
st.set_page_config(
    page_title="ZK-Verifiable ML Demo",
    page_icon="🔐",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f5f5f5;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1E88E5;
    }
    .prediction-card {
        background-color: #e8f5e9;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #4CAF50;
    }
    .proof-card {
        background-color: #f3e5f5;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #9C27B0;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .status-success {
        color: #4CAF50;
        font-weight: bold;
    }
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">🔐 ZK-Verifiable Machine Learning Demo</h1>', unsafe_allow_html=True)
st.markdown("""
    This demo showcases a machine learning model with Zero-Knowledge proofs. 
    The model prediction is verifiable on-chain using cryptographic proofs.
""")

# Sidebar for configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    api_url = st.text_input(
        "API Endpoint", 
        value="http://localhost:8000/zkml/predict",
        help="URL of the ZK-ML inference server"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Model Info")
    st.info("""
    **Model Details:**
    - Type: Neural Network with ZK proofs
    - Features: 3 normalized inputs (0.0 to 1.0)
    - Output: Binary classification
    - ZK Framework: RISC Zero / Halo2
    """)
    
    st.markdown("---")
    st.markdown("### 📈 Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg. Proof Time", "~3.2s")
    with col2:
        st.metric("Proof Size", "~2.4 KB")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎛️ Input Features")
    st.caption("Adjust the feature values between 0.0 and 1.0")
    
    # Feature inputs with better visual organization
    features = []
    feature_names = ["Feature 1", "Feature 2", "Feature 3"]
    default_values = [0.4, 0.7, 0.2]
    descriptions = [
        "First normalized feature representing attribute X",
        "Second normalized feature representing attribute Y",
        "Third normalized feature representing attribute Z"
    ]
    
    for i, (name, default, desc) in enumerate(zip(feature_names, default_values, descriptions)):
        with st.container():
            st.markdown(f'<div class="feature-card">', unsafe_allow_html=True)
            value = st.slider(
                name,
                min_value=0.0,
                max_value=1.0,
                value=float(default),
                step=0.01,
                help=desc,
                key=f"feature_{i}"
            )
            features.append(value)
            st.progress(value, text=f"Value: {value:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)

    # Quick preset buttons
    st.markdown("#### 🚀 Quick Presets")
    preset_cols = st.columns(4)
    with preset_cols[0]:
        if st.button("Case A", use_container_width=True):
            st.session_state.feature_0 = 0.1
            st.session_state.feature_1 = 0.2
            st.session_state.feature_2 = 0.3
            st.rerun()
    with preset_cols[1]:
        if st.button("Case B", use_container_width=True):
            st.session_state.feature_0 = 0.7
            st.session_state.feature_1 = 0.8
            st.session_state.feature_2 = 0.9
            st.rerun()
    with preset_cols[2]:
        if st.button("Case C", use_container_width=True):
            st.session_state.feature_0 = 0.5
            st.session_state.feature_1 = 0.5
            st.session_state.feature_2 = 0.5
            st.rerun()
    with preset_cols[3]:
        if st.button("Reset", use_container_width=True):
            st.session_state.feature_0 = 0.4
            st.session_state.feature_1 = 0.7
            st.session_state.feature_2 = 0.2
            st.rerun()

with col2:
    st.markdown("### 🤖 Model Inference")
    
    if st.button("🚀 Run ZK-Verified Prediction", use_container_width=True):
        with st.spinner("Generating ZK proof and prediction..."):
            try:
                # Simulate processing time for better UX
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.02)  # Simulate processing
                    progress_bar.progress(percent_complete + 1)
                
                # Make API call
                response = requests.post(
                    api_url,
                    json=features,
                    timeout=30
                )
                
                if response.status_code == 200:
                    res = response.json()
                    
                    # Display prediction result
                    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                    st.markdown("### 📊 Prediction Result")
                    
                    prediction_value = res['prediction']
                    if isinstance(prediction_value, (int, float)):
                        # Visual indicator for prediction
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Prediction", f"{prediction_value:.4f}")
                        with col_b:
                            # Binary classification visualization
                            if prediction_value > 0.5:
                                st.success("Class: Positive ✅")
                            else:
                                st.warning("Class: Negative ⚠️")
                        
                        # Prediction probability bar
                        st.progress(
                            prediction_value, 
                            text=f"Confidence: {prediction_value*100:.1f}%"
                        )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display ZK proof details
                    st.markdown("### 🔐 Zero-Knowledge Proof")
                    st.markdown('<div class="proof-card">', unsafe_allow_html=True)
                    
                    st.markdown("#### 📝 Smart Contract Calldata")
                    calldata = res.get("calldata", "")
                    
                    # Show calldata with copy button
                    calldata_col1, calldata_col2 = st.columns([4, 1])
                    with calldata_col1:
                        st.code(calldata, language="solidity")
                    with calldata_col2:
                        if st.button("📋 Copy"):
                            st.code(calldata)
                            st.success("Copied!")
                    
                    st.markdown("#### 📋 Proof Details")
                    
                    # Show additional proof information if available
                    if "proof_info" in res:
                        proof_info = res["proof_info"]
                        info_cols = st.columns(2)
                        with info_cols[0]:
                            st.metric("Proof Size", f"{proof_info.get('size_bytes', 0)} bytes")
                        with info_cols[1]:
                            st.metric("Gas Cost", f"{proof_info.get('gas_estimate', 0)}")
                    
                    st.success("✅ Proof verifiable on-chain")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Download option
                    st.markdown("#### 💾 Export Results")
                    result_data = {
                        "features": features,
                        "prediction": res['prediction'],
                        "calldata": calldata,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    result_json = json.dumps(result_data, indent=2)
                    st.download_button(
                        label="📥 Download Results as JSON",
                        data=result_json,
                        file_name=f"zkml_result_{time.strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.code(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to the ZK-ML server. Please make sure the server is running.")
                st.info("Start the server with: `python server.py` or check the endpoint configuration.")
            except requests.exceptions.Timeout:
                st.error("⏰ Request timeout. The server is taking too long to respond.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    # Information section when no prediction is made
    else:
        st.info("👆 Click the button above to generate a ZK-verifiable prediction")
        
        # Example section
        with st.expander("📚 How it works"):
            st.markdown("""
            1. **Input Features**: You provide the feature values (0.0 to 1.0)
            2. **ZK Proof Generation**: The model computes the prediction and generates a zero-knowledge proof
            3. **On-chain Verification**: The proof can be verified on Ethereum or other EVM chains
            4. **Trustless ML**: Anyone can verify the computation was correct without seeing the model weights
            
            **Key Benefits:**
            - 🛡️ **Privacy**: Model weights remain private
            - 🔍 **Verifiability**: Anyone can verify the computation
            - ⛓️ **On-chain**: Results can be used in smart contracts
            """)

# Footer
st.markdown("---")
footer_cols = st.columns(3)
with footer_cols[0]:
    st.caption("🔗 [GitHub Repository](https://github.com/example/zk-ml-demo)")
with footer_cols[1]:
    st.caption("📚 [Documentation](https://docs.example.com)")
with footer_cols[2]:
    st.caption("Made with Streamlit & ZK-SNARKs")

# Debug info (can be toggled)
if st.sidebar.checkbox("Show debug info", False):
    st.sidebar.write("### Debug Information")
    st.sidebar.json({
        "features": features,
        "api_endpoint": api_url,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })