@echo off
echo ================================================================
echo 🚀 Starting ZK-ML Full System
echo ================================================================
echo.

echo 1. Starting Hardhat Local Node...
start "Hardhat Node" cmd /k "cd /d blockchain && npx hardhat node"
timeout /t 25 /nobreak >nul

echo.
echo 2. Deploying Smart Contracts...
start "Contract Deploy" cmd /k "cd /d blockchain && npx hardhat run scripts/deploy.js --network localhost"
timeout /t 20 /nobreak >nul

echo.
echo 3. Starting FastAPI Backend...
start "FastAPI Server" cmd /k "uvicorn api.main:app --reload --port 8000"
timeout /t 20 /nobreak >nul

echo.
echo 4. Starting Streamlit Dashboard...
start "Streamlit App" cmd /k "streamlit run streamlit_app.py --server.port 8501"

echo.
echo ================================================================
echo ✅ All services started successfully!
echo ================================================================
echo.
echo 📊 Services Status:
echo 1. Hardhat Node     : http://localhost:8545
echo 2. FastAPI Backend  : http://localhost:8000
echo 3. Streamlit Dashboard : http://localhost:8501
echo 4. FastAPI Docs     : http://localhost:8000/docs
echo.
echo 🛑 Close all terminal windows to stop services
echo ================================================================
pause