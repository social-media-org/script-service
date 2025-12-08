#!/usr/bin/env python3
"""
Start script for Script Generation Service using its virtual environment.
This script ensures the virtual environment is activated and dependencies are installed.
"""

import os
import sys
import subprocess
import platform

def main():
    # Determine the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = script_dir
    
    # Virtual environment paths
    venv_dir = os.path.join(project_root, ".venv")
    
    # Check if virtual environment exists
    if not os.path.exists(venv_dir):
        print(f"Virtual environment not found at {venv_dir}")
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        print("Virtual environment created.")
    
    # Determine the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_exe = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        python_exe = os.path.join(venv_dir, "bin", "python")
        pip_exe = os.path.join(venv_dir, "bin", "pip")
    
    # Check if requirements are installed
    print("Checking dependencies...")
    requirements_file = os.path.join(project_root, "requirements.txt")
    
    # Install requirements if needed
    if os.path.exists(requirements_file):
        print(f"Installing requirements from {requirements_file}")
        result = subprocess.run([pip_exe, "install", "-r", requirements_file], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to install requirements: {result.stderr}")
            sys.exit(1)
        print("Requirements installed successfully.")
    
    # Now run the application using the virtual environment Python
    print(f"Starting Script Generation Service using virtual environment at {venv_dir}")
    
    # Change to project directory
    os.chdir(project_root)
    
    # Run uvicorn through the virtual environment Python
    app_command = [
        python_exe, "-m", "uvicorn", "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8002"
    ]
    
    print(f"Running command: {' '.join(app_command)}")
    print(f"Service will be available at http://localhost:8002")
    print(f"API documentation: http://localhost:8002/docs")
    print("Press Ctrl+C to stop the server.")
    
    # Execute the command
    subprocess.run(app_command)

if __name__ == "__main__":
    main()
