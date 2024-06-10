import subprocess
import sys

class Setup:
    def install(self, package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    def install_required_packages(self):
        # List of required packages
        required_packages = [
            "bcrypt",
            "cryptography"
        ]

        # Install required packages
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                print(f"Installing {package}...")
                self.install(package)
                print(f"{package} installed successfully.")

if __name__ == "__main__":
    setup = Setup()
    setup.install_required_packages()