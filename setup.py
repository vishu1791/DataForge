"""
Setup script for the Data Cleaning Tool.
Run this script to install dependencies and verify the installation.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("📁 Creating necessary directories...")
    directories = [
        "data/raw",
        "data/processed", 
        "outputs/plots",
        "outputs/reports",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}")

def test_imports():
    """Test if all modules can be imported."""
    print("🧪 Testing imports...")
    
    modules_to_test = [
        "streamlit",
        "pandas", 
        "numpy",
        "matplotlib",
        "seaborn",
        "plotly",
        "sklearn",
        "openpyxl",
        "pyarrow"
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️ Failed to import: {', '.join(failed_imports)}")
        print("Please install these packages manually.")
        return False
    else:
        print("\n🎉 All packages imported successfully!")
        return True

def main():
    """Main setup function."""
    print("🚀 Setting up Data Cleaning Tool...")
    print("=" * 50)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("\n❌ Setup failed at package installation.")
        return
    
    # Step 2: Create directories
    create_directories()
    
    # Step 3: Test imports
    if not test_imports():
        print("\n❌ Setup failed at import testing.")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the test script: python test_app.py")
    print("2. Start the application: streamlit run app.py")
    print("3. Open your browser and go to: http://localhost:8501")

if __name__ == "__main__":
    main()
