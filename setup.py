#!/usr/bin/env python3
"""
Setup script for Medical AI Bot
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python 3.8+ is installed"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def setup_env_file():
    """Set up environment file"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("📝 Creating .env file from .env.example...")
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✅ .env file created")
            print("⚠️  Please edit .env file and add your OpenAI API key")
        else:
            print("📝 Creating .env file...")
            with open(".env", "w") as f:
                f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
                f.write("OPENAI_MODEL=gpt-3.5-turbo\n")
            print("✅ .env file created")
            print("⚠️  Please edit .env file and add your OpenAI API key")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🩺 Medical AI Bot Setup")
    print("=" * 30)
    
    if not check_python_version():
        return False
    
    if not install_requirements():
        return False
    
    setup_env_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: streamlit run app.py")
    print("3. Open your browser to http://localhost:8501")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)