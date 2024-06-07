import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = [
    "bcrypt"
]

# Install required packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)