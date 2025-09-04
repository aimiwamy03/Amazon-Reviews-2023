"""
Setup script for AI Consumer Insights Platform
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def download_spacy_model():
    """Download spaCy model (optional)"""
    print("📥 Downloading spaCy model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_lg"])
        print("✅ spaCy model downloaded successfully!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Warning: Could not download spaCy model: {e}")
        print("   The platform will still work, but some advanced NLP features may be limited.")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = ["outputs", "models", "data"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   Created: {directory}/")
        else:
            print(f"   Exists: {directory}/")

def main():
    """Main setup function"""
    print("🚀 Setting up AI Consumer Insights Platform...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return
    
    # Download spaCy model
    download_spacy_model()
    
    # Create directories
    create_directories()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    print("1. Run: streamlit run main.py")
    print("2. Open: http://localhost:8501")
    print("3. Click 'Load Sample Data' to start analyzing")
    print("\n💡 For advanced features, add your OpenAI API key to config.py")

if __name__ == "__main__":
    main()
