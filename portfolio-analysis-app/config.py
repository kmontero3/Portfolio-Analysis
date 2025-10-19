import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SCHWAB_API_KEY = os.environ.get('SCHWAB_API_KEY') or 'your_schwab_api_key'
    SCHWAB_API_SECRET = os.environ.get('SCHWAB_API_SECRET') or 'your_schwab_api_secret'
    SCHWAB_API_BASE_URL = 'https://api.schwab.com'  # Base URL for Schwab API
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Enable or disable debug mode based on environment variable