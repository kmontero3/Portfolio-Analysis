# Portfolio Analysis Application

## Introduction

This Portfolio Analysis Application is a Flask-based web application designed to provide investment portfolio analysis and visualization capabilities. Built on top of the Schwab Developer API platform, this application enables investors to securely access, analyze, and visualize their investment portfolios in real-time.

The application implements industry-standard OAuth 2.0 authentication protocols to ensure secure access to sensitive financial data, while providing an intuitive interface for portfolio tracking, risk assessment, and performance analysis. Whether you're an individual investor managing your personal portfolio or a financial professional requiring detailed analytics, this application provides the tools necessary for informed investment decision-making.

## Key Features

- **Secure OAuth 2.0 Authentication**: Industry-standard authentication protocol with Schwab API
- **Real-time Portfolio Data**: Live portfolio data retrieval and synchronization
- **Multi-Account Support**: Manage and analyze multiple investment accounts simultaneously
- **Automatic Token Management**: Seamless token refresh and session management
- **Portfolio Analysis Tools**: Comprehensive investment analysis and visualization capabilities
- **Secure Credential Management**: Environment-based configuration for sensitive credentials
- **HTTPS Support**: Secure local development environment with SSL/TLS encryption

## Overview

This application serves as a bridge between your Schwab brokerage account and advanced portfolio analysis tools. By leveraging the Schwab Developer API, the application provides:

- Real-time access to account balances and positions
- Historical order data and transaction history
- Portfolio performance metrics and analytics
- Risk assessment and diversification analysis
- Customizable reporting and data visualization

The application is designed with security as a primary concern, implementing best practices for credential management, secure communication, and data protection.

## Project Structure
```
portfolio-analysis-app/
├── app.py                      # Entry point of the Flask application
├── config.py                   # Configuration with environment variable management
├── requirements.txt            # Python dependencies
├── test_schwab_connection.py   # Connectivity test script
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules for security
├── static/                     # Static frontend files
│   ├── css/
│   │   └── style.css          # Application styles
│   └── js/
│       └── app.js             # Frontend JavaScript
├── templates/                  # HTML templates
│   └── index.html             # Main application interface
├── api/                        # API integration layer
│   ├── __init__.py
│   ├── routes.py              # Flask API routes
│   └── schwab_client.py       # Schwab API OAuth 2.0 client
└── helpers/                    # Business logic and utilities
    ├── __init__.py
    ├── portfolio_analyzer.py  # Portfolio analysis functions
    └── data_processor.py      # Data processing utilities
```

## Prerequisites

- Python 3.8 or higher
- Schwab Developer Account with API credentials
- Git version control system
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Technology Stack

- **Backend Framework**: Flask 3.0+
- **Authentication**: OAuth 2.0
- **API Integration**: Schwab Developer API
- **Security**: SSL/TLS encryption, environment-based configuration
- **Data Format**: JSON

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kmontero3/Portfolio-Analysis.git
cd portfolio-analysis-app
```

### 2. Create Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies from your system Python installation.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Obtain Schwab API Credentials

#### Step 1: Create a Schwab Developer Account

1. Navigate to the Schwab Developer Portal: https://developer.schwab.com/
2. Click "Register" to create a new developer account
3. Complete the registration process and verify your email address

#### Step 2: Create an Application

1. Log in to the Developer Portal
2. Navigate to "My Apps" section
3. Click "Create New App"
4. Complete the application form with the following information:
   - **Application Name**: Portfolio Analysis Application (or your preferred name)
   - **Redirect URI**: `https://127.0.0.1:5000/callback`
   - **Description**: Portfolio analysis and visualization application
5. Submit the application for approval

#### Step 3: Retrieve Your Credentials

After application approval, you will receive:
- **App Key** (Client ID): Your unique application identifier
- **App Secret** (Client Secret): Your application's secret key

**Important**: Store these credentials securely and never commit them to version control.

### 5. Configure Environment Variables

#### Step 1: Create Environment File

Copy the example environment file to create your configuration:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

#### Step 2: Configure Credentials

Edit the `.env` file and update it with your actual Schwab API credentials:

```env
# Schwab API Credentials
SCHWAB_API_KEY=your_actual_app_key_here
SCHWAB_API_SECRET=your_actual_app_secret_here
SCHWAB_REDIRECT_URI=https://127.0.0.1:5000/callback

# Flask Configuration
FLASK_SECRET_KEY=your_generated_secret_key_here
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

#### Step 3: Generate Flask Secret Key

Generate a cryptographically secure secret key for Flask session management:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as your `FLASK_SECRET_KEY` in the `.env` file.

### 6. Generate SSL Certificates for HTTPS

Schwab's OAuth implementation requires HTTPS for redirect URIs. Generate self-signed SSL certificates for local development:

```bash
python generate_ssl_cert.py
```

This will create:
- `cert.pem`: SSL certificate
- `key.pem`: Private key

**Note**: Your browser will display a security warning when accessing the application. This is normal for self-signed certificates. You can safely proceed by clicking "Advanced" and "Proceed to 127.0.0.1".

### 7. Test API Connection

Before running the full application, verify your Schwab API setup:

```bash
python test_schwab_connection.py
```

This diagnostic script will:
- Validate your environment configuration
- Initialize the Schwab API client
- Guide you through the OAuth authentication process
- Test API connectivity
- Display available permissions and scopes
- Retrieve basic account information

#### First-Time Authentication Process

1. The script will automatically open your default web browser
2. Log in to your Schwab brokerage account
3. Authorize the application to access your portfolio data
4. You will be redirected to the callback URL with an authorization code
5. The application will automatically exchange the code for access tokens
6. Your authentication tokens will be securely saved for future use

### 8. Run the Application

Start the Flask development server:

```bash
python app.py
```

The application will be accessible at: `https://127.0.0.1:5000`

**Server Output:**
```
============================================================
  Portfolio Analysis Application - Development Server
============================================================
  Environment: development
  Debug Mode: True
============================================================

SSL certificates found - Running with HTTPS
  Server: https://127.0.0.1:5000
```

## Configuration Reference

### Environment Variables

The application uses environment variables for configuration management. All sensitive configuration should be stored in the `.env` file, which is excluded from version control.

| Variable | Description | Required | Default Value |
|----------|-------------|----------|---------------|
| `SCHWAB_API_KEY` | Schwab App Key (Client ID) | Yes | - |
| `SCHWAB_API_SECRET` | Schwab App Secret (Client Secret) | Yes | - |
| `SCHWAB_REDIRECT_URI` | OAuth redirect URI | Yes | `https://127.0.0.1:5000/callback` |
| `SCHWAB_ACCOUNT_HASH` | Encrypted account hash for orders API | No | - |
| `FLASK_SECRET_KEY` | Flask session encryption key | Yes | Auto-generated (dev only) |
| `FLASK_ENV` | Application environment | No | `development` |
| `FLASK_DEBUG` | Enable debug mode | No | `True` |
| `FLASK_HOST` | Server host address | No | `127.0.0.1` |
| `FLASK_PORT` | Server port number | No | `5000` |
| `LOG_LEVEL` | Logging verbosity level | No | `INFO` |

### Security Best Practices

#### Credential Management

1. **Never commit sensitive files to version control:**
   - `.env` file (contains API credentials)
   - `schwab_tokens.json` (contains access and refresh tokens)
   - `cert.pem` and `key.pem` (SSL certificates)
   - These files are already included in `.gitignore`

2. **Use HTTPS in production environments:**
   - Configure proper SSL/TLS certificates
   - Update `SCHWAB_REDIRECT_URI` to use your production domain
   - Never use self-signed certificates in production

3. **Implement credential rotation:**
   - Periodically generate new API keys from the Schwab Developer Portal
   - Update the `.env` file with new credentials
   - Regenerate Flask secret keys regularly

4. **Use strong cryptographic keys:**
   - Always generate secret keys using cryptographically secure random number generators
   - Never use default, example, or weak keys in any environment
   - Use different keys for development, staging, and production environments

5. **Secure token storage:**
   - The application stores OAuth tokens in `schwab_tokens.json`
   - This file is automatically excluded from version control
   - Ensure proper file system permissions on production servers

#### API Security

1. **Token Management:**
   - Access tokens expire after 30 minutes
   - Refresh tokens expire after 7 days
   - The application automatically handles token refresh
   - Re-authentication is required when refresh tokens expire

2. **Rate Limiting:**
   - Be mindful of Schwab API rate limits
   - Implement appropriate caching mechanisms
   - Handle 429 (rate limit exceeded) errors gracefully

3. **Data Protection:**
   - All API communication uses HTTPS
   - Session data is encrypted using Flask's secret key
   - Sensitive data should never be logged or exposed in error messages

## API Usage

### SchwabClient Interface

The `SchwabClient` class provides a Python interface to the Schwab Developer API with built-in OAuth 2.0 authentication and token management.

#### Basic Usage Example

```python
from app.blueprints.api.schwab_integration import SchwabClient
from config import Config

# Initialize the client
client = SchwabClient(
    api_key=Config.SCHWAB_API_KEY,
    api_secret=Config.SCHWAB_API_SECRET,
    redirect_uri=Config.SCHWAB_REDIRECT_URI
)

# Authenticate (handles OAuth flow automatically)
client.authenticate()

# Retrieve account numbers
accounts = client.get_account_numbers()

# Get detailed account data with positions
account_data = client.get_account_data(fields="positions")

# Get portfolio data (convenience method)
portfolio = client.get_portfolio_data()

# Test connectivity and display status
client.print_connection_status()
```

#### Error Handling

```python
from app.blueprints.api.schwab_integration import SchwabAPIError

try:
    client.authenticate()
    data = client.get_portfolio_data()
    # Process portfolio data
except SchwabAPIError as e:
    print(f"API Error: {e}")
    # Handle API-specific errors
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle general errors
```

### Available API Methods

#### Authentication Methods

- `authenticate(authorization_code=None, auto_open_browser=True)`: Handles complete OAuth flow
- `get_authorization_url()`: Generates OAuth authorization URL
- `refresh_access_token()`: Refreshes expired access tokens
- `test_connectivity()`: Tests API connectivity and authentication status

#### Data Retrieval Methods

- `get_account_numbers()`: Retrieves all account numbers with encrypted hashes
- `get_account_data(account_hash=None, fields=None)`: Gets account data and balances
- `get_portfolio_data(account_hash=None)`: Retrieves complete portfolio with positions
- `get_user_preferences()`: Fetches user preferences and settings

#### Utility Methods

- `print_connection_status()`: Displays detailed connection and authentication status

## Development

### Running Tests

```bash
# Test Schwab API connectivity
python test_schwab_connection.py

# Run unit tests (if configured)
# pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. To format code:

```bash
# Install black (optional)
pip install black

# Format code
black .
```

### Logging

The application uses Python's built-in logging module. Configure log level in `.env`:

```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```


## Development

### Project Architecture

The application follows a modular architecture with clear separation of concerns:

```
portfolio-analysis-app/
├── app/                          # Core application package
│   ├── blueprints/               # Flask blueprints for routing
│   │   ├── api/                  # API endpoints and integrations
│   │   │   ├── schwab_integration.py  # Schwab API client
│   │   │   ├── routes_auth.py    # Authentication routes
│   │   │   ├── routes_overview.py # Portfolio overview routes
│   │   │   └── routes_risk.py    # Risk analysis routes
│   │   └── ui/                   # User interface routes
│   │       ├── routes.py         # UI route definitions
│   │       ├── static/           # CSS, JavaScript assets
│   │       └── templates/        # Jinja2 HTML templates
│   ├── services/                 # Business logic services
│   │   ├── prices.py             # Price data management
│   │   ├── returns.py            # Return calculations
│   │   └── risk.py               # Risk metrics computation
│   └── extensions.py             # Flask extensions initialization
├── data/                         # Data storage directory
│   └── schwab/                   # Schwab API response cache
├── config.py                     # Configuration management
└── app.py                        # Application entry point
```

### Code Style Guidelines

This project follows industry-standard Python coding conventions:

1. **PEP 8 Compliance**: Follow PEP 8 style guide for Python code
   - Use 4 spaces for indentation (no tabs)
   - Limit lines to 79 characters for code, 72 for comments/docstrings
   - Use snake_case for function and variable names
   - Use PascalCase for class names

2. **Docstrings**: Use Google-style docstrings for all functions and classes
   ```python
   def calculate_portfolio_value(positions: list, prices: dict) -> float:
       """Calculates total portfolio value from positions and current prices.
       
       Args:
           positions: List of position dictionaries with symbol and quantity
           prices: Dictionary mapping symbols to current prices
           
       Returns:
           Total portfolio value as a float
           
       Raises:
           ValueError: If positions list is empty or prices missing
       """
   ```

3. **Type Hints**: Use type hints for function parameters and return values
   ```python
   from typing import Dict, List, Optional
   
   def get_account_data(account_hash: Optional[str] = None) -> Dict[str, any]:
       pass
   ```

4. **Import Organization**:
   - Standard library imports first
   - Third-party library imports second
   - Local application imports last
   - Group imports alphabetically within each section

5. **Error Handling**: Use specific exception types and meaningful error messages
   ```python
   try:
       response = requests.get(url, headers=headers)
       response.raise_for_status()
   except requests.HTTPError as e:
       raise SchwabAPIError(f"API request failed: {e}")
   ```

### Testing

#### Unit Tests

Run unit tests using pytest:

```bash
pytest tests/
```

#### API Integration Tests

Test Schwab API connectivity:

```bash
# Test basic connectivity
python test_schwab_connection.py

# Test specific endpoints
python test_schwab_api.py

# Test simplified API calls
python test_schwab_simple.py
```

#### Manual Testing Workflow

1. Start the Flask application: `python app.py`
2. Navigate to `https://127.0.0.1:5000/login`
3. Complete OAuth authentication flow
4. Verify data fetching: `python fetch_schwab_data.py`
5. Check saved data in `data/schwab/` directory

### Adding New Features

When implementing new features, follow this workflow:

1. **Plan**: Document requirements and design approach
2. **Branch**: Create a feature branch from main
3. **Develop**: Implement feature following code style guidelines
4. **Test**: Write and run tests for new functionality
5. **Document**: Update README and code docstrings
6. **Review**: Ensure code quality and security best practices
7. **Merge**: Submit pull request for review

### API Rate Limits

The Schwab API enforces rate limits to prevent abuse:

- **Rate Limit Policy**: Specific limits vary by endpoint and account type
- **Best Practices**:
  - Implement exponential backoff for retries
  - Cache responses where appropriate
  - Batch requests when possible
  - Monitor response headers for rate limit information

- **Handling 429 Errors**:
  ```python
  import time
  from requests.exceptions import HTTPError
  
  def make_request_with_retry(url, max_retries=3):
      for attempt in range(max_retries):
          try:
              response = requests.get(url)
              response.raise_for_status()
              return response.json()
          except HTTPError as e:
              if e.response.status_code == 429:
                  wait_time = 2 ** attempt  # Exponential backoff
                  time.sleep(wait_time)
              else:
                  raise
      raise Exception("Max retries exceeded")
  ```

### Security Considerations

When developing features that interact with sensitive data:

1. **Never Log Credentials**: Avoid logging API keys, tokens, or account numbers
2. **Validate Input**: Sanitize all user input to prevent injection attacks
3. **Use HTTPS**: Always use HTTPS for API communications
4. **Token Storage**: Store tokens securely and encrypt at rest if possible
5. **Access Control**: Implement proper authentication and authorization
6. **Audit Trail**: Log access to sensitive operations

### Debugging Tips

1. **Enable Flask Debug Mode** (development only):
   ```python
   # In app.py
   app.run(debug=True, ssl_context=context)
   ```

2. **Verbose Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **API Request Inspection**:
   ```python
   # Add to schwab_integration.py for debugging
   print(f"Request URL: {response.url}")
   print(f"Request Headers: {response.request.headers}")
   print(f"Response Status: {response.status_code}")
   print(f"Response Body: {response.text}")
   ```

4. **Token Examination**:
   ```bash
   python -c "import json; print(json.dumps(json.load(open('schwab_tokens.json')), indent=2))"
   ```