"""
Quick Start Script for Schwab API Setup

This script helps you quickly set up and test your Schwab API integration.
Run this after installing dependencies and configuring your .env file.
"""

import os
import sys
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def print_step(number, text):
    """Print a step indicator"""
    print(f"\n{'='*80}")
    print(f"STEP {number}: {text}")
    print('='*80 + "\n")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✓ {description} found")
        return True
    else:
        print(f"✗ {description} NOT found")
        return False

def main():
    print_header("SCHWAB API SETUP - QUICK START")
    
    # Check Python version
    print_step(1, "Checking Python Version")
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major >= 3 and python_version.minor >= 8:
        print("✓ Python version is compatible (3.8+)")
    else:
        print("✗ Python version is too old. Please upgrade to 3.8 or higher.")
        return 1
    
    # Check required files
    print_step(2, "Checking Required Files")
    files_ok = True
    files_ok &= check_file_exists("requirements.txt", "requirements.txt")
    files_ok &= check_file_exists("config.py", "config.py")
    files_ok &= check_file_exists("api/schwab_client.py", "schwab_client.py")
    files_ok &= check_file_exists(".env.example", ".env.example")
    files_ok &= check_file_exists("test_schwab_connection.py", "test_schwab_connection.py")
    
    if not files_ok:
        print("\n✗ Some required files are missing!")
        return 1
    
    # Check if .env exists
    print_step(3, "Checking Environment Configuration")
    if not check_file_exists(".env", ".env file"):
        print("\n⚠️  .env file not found!")
        print("\nPlease create it by running:")
        if sys.platform == "win32":
            print("    copy .env.example .env")
        else:
            print("    cp .env.example .env")
        print("\nThen edit .env and add your Schwab API credentials.")
        print("\nTo get Schwab API credentials:")
        print("1. Go to https://developer.schwab.com/")
        print("2. Create a developer account")
        print("3. Create a new app")
        print("4. Copy your App Key and App Secret to .env")
        return 1
    
    # Check dependencies
    print_step(4, "Checking Dependencies")
    try:
        import flask
        print("✓ Flask installed")
    except ImportError:
        print("✗ Flask not installed")
        print("\nPlease install dependencies:")
        print("    pip install -r requirements.txt")
        return 1
    
    try:
        import requests
        print("✓ requests installed")
    except ImportError:
        print("✗ requests not installed")
        print("\nPlease install dependencies:")
        print("    pip install -r requirements.txt")
        return 1
    
    try:
        import dotenv
        print("✓ python-dotenv installed")
    except ImportError:
        print("✗ python-dotenv not installed")
        print("\nPlease install dependencies:")
        print("    pip install -r requirements.txt")
        return 1
    
    # Try to load config
    print_step(5, "Loading Configuration")
    try:
        from config import Config
        Config.print_config_status(show_secrets=False)
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return 1
    
    # Validate config
    print_step(6, "Validating Configuration")
    try:
        from config import Config
        Config.validate_required_config()
        print("✓ All required configuration is set")
    except Exception as e:
        print(f"✗ Configuration validation failed:\n{e}")
        print("\nPlease update your .env file with valid credentials.")
        return 1
    
    # All checks passed
    print_header("SETUP COMPLETE!")
    print("All checks passed! You're ready to test the Schwab API connection.\n")
    print("Next steps:")
    print("1. Run the connectivity test:")
    print("   python test_schwab_connection.py")
    print()
    print("2. If the test succeeds, start the Flask application:")
    print("   python app.py")
    print()
    print("Need help?")
    print("- Check README.md for detailed instructions")
    print("- Review IMPLEMENTATION_SUMMARY.md for technical details")
    print("- Visit https://developer.schwab.com/ for API documentation")
    print()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
