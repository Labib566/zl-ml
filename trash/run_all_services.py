import subprocess
import time
import os
import sys
import threading
import signal

def run_command_in_terminal(command, cwd=None, shell=False):
    """একটি কমান্ড রান করে এবং আউটপুট দেখায়"""
    try:
        print(f"\n🚀 Running: {command}")
        process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # রিয়েল-টাইম আউটপুট দেখানোর জন্য থ্রেড
        def print_output():
            for line in process.stdout:
                print(f"[{command.split()[0]}] {line}", end='')
        
        output_thread = threading.Thread(target=print_output)
        output_thread.daemon = True
        output_thread.start()
        
        return process
    except Exception as e:
        print(f"❌ Error running {command}: {e}")
        return None

def main():
    print("="*60)
    print("🚀 ZK-ML Full System Automation Script")
    print("="*60)
    
    # বর্তমান ডিরেক্টরি
    root_dir = os.getcwd()
    blockchain_dir = os.path.join(root_dir, "blockchain")
    
    processes = []
    
    try:
        # 1. হার্ডহ্যাট নোড চালু
        print("\n" + "="*60)
        print("📡 Starting Hardhat Local Node...")
        print("="*60)
        process1 = run_command_in_terminal(
            ["npx", "hardhat", "node"],
            cwd=blockchain_dir,
            shell=False
        )
        processes.append(process1)
        time.sleep(25)  # নোড সম্পূর্ণ চালু হতে সময় দিন
        
        # 2. কন্ট্রাক্ট ডেপ্লয়
        print("\n" + "="*60)
        print("📦 Deploying Smart Contracts...")
        print("="*60)
        process2 = run_command_in_terminal(
            ["npx", "hardhat", "run", "scripts/deploy.js", "--network", "localhost"],
            cwd=blockchain_dir,
            shell=False
        )
        processes.append(process2)
        time.sleep(20)  # ডেপ্লয় সম্পূর্ণ হতে সময় দিন
        
        # 3. FastAPI সার্ভার চালু
        print("\n" + "="*60)
        print("🌐 Starting FastAPI Backend...")
        print("="*60)
        process3 = run_command_in_terminal(
            ["uvicorn", "api.main:app", "--reload", "--port", "8000"],
            cwd=root_dir,
            shell=False
        )
        processes.append(process3)
        time.sleep(20)  # API সার্ভার চালু হতে সময় দিন
        
        # 4. Streamlit অ্যাপ চালু
        print("\n" + "="*60)
        print("🎨 Starting Streamlit Dashboard...")
        print("="*60)
        process4 = run_command_in_terminal(
            ["streamlit", "run", "streamlit_app.py", "--server.port", "8501"],
            cwd=root_dir,
            shell=False
        )
        processes.append(process4)
        
        print("\n" + "="*60)
        print("✅ All services started successfully!")
        print("="*60)
        print("\n📊 Services Status:")
        print("1. Hardhat Node     : http://localhost:8545")
        print("2. FastAPI Backend  : http://localhost:8000")
        print("3. Streamlit Dashboard : http://localhost:8501")
        print("4. FastAPI Docs     : http://localhost:8000/docs")
        print("\n🛑 Press Ctrl+C to stop all services")
        print("="*60)
        
        # সব প্রসেস চলতে রাখা
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all services...")
        
        # সব প্রসেস বন্ধ করা
        for i, process in enumerate(processes):
            if process and process.poll() is None:
                print(f"Stopping process {i+1}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✅ All services stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()