"""
Configuration module for Portfolio Analysis Application

Loads configuration from environment variables with validation.
Uses python-dotenv to load .env file for local development.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid"""
    pass


class Config:
    """
    Application configuration class.
    
    Loads configuration from environment variables with validation.
    Required variables are validated at startup to fail fast.
    """
    
    # ===========================
    # FLASK CONFIGURATION
    # ===========================
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        # Generate a random secret key for development
        import secrets
        SECRET_KEY = secrets.token_hex(32)
        logger.warning("No FLASK_SECRET_KEY set. Using generated key (not suitable for production)")
    
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    ENV = os.environ.get('FLASK_ENV', 'development')
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # ===========================
    # SCHWAB API CONFIGURATION
    # ===========================
    SCHWAB_API_KEY = os.environ.get('SCHWAB_API_KEY')
    SCHWAB_API_SECRET = os.environ.get('SCHWAB_API_SECRET')
    SCHWAB_REDIRECT_URI = os.environ.get('SCHWAB_REDIRECT_URI', 'https://127.0.0.1:5000/callback')
    SCHWAB_API_BASE_URL = 'https://api.schwabapi.com'
    
    # ===========================
    # LOGGING CONFIGURATION
    # ===========================
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
    ENABLE_DEBUG_LOGGING = os.environ.get('ENABLE_DEBUG_LOGGING', 'False').lower() in ('true', '1', 'yes')
    
    # ===========================
    # APPLICATION SETTINGS
    # ===========================
    # Token storage file
    TOKEN_FILE = 'schwab_tokens.json'
    
    @classmethod
    def validate_required_config(cls) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            True if all required config is valid
            
        Raises:
            ConfigurationError: If required configuration is missing
        """
        errors = []
        
        # Check Schwab API credentials
        if not cls.SCHWAB_API_KEY:
            errors.append("SCHWAB_API_KEY is not set in environment variables")
        
        if not cls.SCHWAB_API_SECRET:
            errors.append("SCHWAB_API_SECRET is not set in environment variables")
        
        if not cls.SCHWAB_REDIRECT_URI:
            errors.append("SCHWAB_REDIRECT_URI is not set in environment variables")
        
        # Check Flask secret key in production
        if cls.ENV == 'production' and not os.environ.get('FLASK_SECRET_KEY'):
            errors.append("FLASK_SECRET_KEY must be set in production environment")
        
        if errors:
            error_message = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ConfigurationError(error_message)
        
        return True
    
    @classmethod
    def print_config_status(cls, show_secrets: bool = False) -> None:
        """
        Print the current configuration status.
        
        Args:
            show_secrets: If True, show partial values of secrets (for debugging)
        """
        def mask_secret(value: str, show_chars: int = 4) -> str:
            """Mask a secret value, showing only first few characters"""
            if not value:
                return "NOT SET"
            if show_secrets:
                if len(value) <= show_chars:
                    return value
                return f"{value[:show_chars]}...{value[-show_chars:]}"
            return "***SET***"
        
        print("\n" + "="*80)
        print("CONFIGURATION STATUS")
        print("="*80 + "\n")
        
        print(f"Flask Environment: {cls.ENV}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"Host: {cls.HOST}")
        print(f"Port: {cls.PORT}")
        print(f"Secret Key: {mask_secret(cls.SECRET_KEY)}")
        print()
        print(f"Schwab API Key: {mask_secret(cls.SCHWAB_API_KEY)}")
        print(f"Schwab API Secret: {mask_secret(cls.SCHWAB_API_SECRET)}")
        print(f"Schwab Redirect URI: {cls.SCHWAB_REDIRECT_URI}")
        print(f"Schwab Base URL: {cls.SCHWAB_API_BASE_URL}")
        print()
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Debug Logging: {cls.ENABLE_DEBUG_LOGGING}")
        
        print("\n" + "="*80 + "\n")
        
        # Try validation
        try:
            cls.validate_required_config()
            print("✓ All required configuration is set\n")
        except ConfigurationError as e:
            print(f"✗ Configuration validation failed:\n{e}\n")


class DevelopmentConfig(Config):
    """Development-specific configuration"""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Production-specific configuration"""
    DEBUG = False
    ENV = 'production'


class TestingConfig(Config):
    """Testing-specific configuration"""
    TESTING = True
    ENV = 'testing'


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env_name: str = None) -> Config:
    """
    Get configuration object based on environment name.
    
    Args:
        env_name: Environment name (development, production, testing)
                 If None, uses FLASK_ENV environment variable
    
    Returns:
        Configuration object
    """
    if env_name is None:
        env_name = os.environ.get('FLASK_ENV', 'development')
    
    return config_by_name.get(env_name, DevelopmentConfig)