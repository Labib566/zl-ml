# পুরনো প্রসেসগুলো বন্ধ করার ফাংশন
function Stop-PortProcess($port) {
    $process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "Cleaning up port $port..." -ForegroundColor Yellow
        Stop-Process -Id $process.OwningProcess -Force
    }
}

# পোর্ট ক্লিয়ার করা
Stop-PortProcess 8545
Stop-PortProcess 8000
Stop-PortProcess 8501

$activateVenv = ".\.venv\Scripts\Activate.ps1"

# ১. Hardhat Node
Write-Host "1. Starting Hardhat Node..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd blockchain; npx hardhat node"
Start-Sleep -Seconds 5

# ২. Deploy Contract
Write-Host "2. Deploying Smart Contract..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd blockchain; npx hardhat run scripts/deploy.js --network localhost"
Start-Sleep -Seconds 5

# ৩. FastAPI (Uvicorn) এবং অটো-ব্রাউজার ওপেন
Write-Host "3. Starting FastAPI Server & Opening Browser..." -ForegroundColor Cyan
# এখানে উবিকর্ন রান করার সাথে সাথে ব্রাউজারে লিঙ্কটি ওপেন হবে
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& $activateVenv; Start-Process 'http://127.0.0.1:8000/docs'; uvicorn api.main:app --reload --port 8000"
Start-Sleep -Seconds 20

# ৪. Streamlit App
Write-Host "4. Starting Streamlit App..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& $activateVenv; streamlit run streamlit_app.py"

Write-Host "All processes started successfully!" -ForegroundColor Green