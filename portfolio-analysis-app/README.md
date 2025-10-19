# Portfolio Analysis App

## Overview
The Portfolio Analysis App is a Flask-based web application designed to analyze and visualize investment portfolios using data retrieved from the Schwab Developer APIs. This application provides a secure, user-friendly interface with OAuth 2.0 authentication to access real-time portfolio data and provide comprehensive investment insights.

## Features
- 🔐 Secure OAuth 2.0 authentication with Schwab API
- 📊 Real-time portfolio data retrieval
- 💼 Multi-account support
- 🔄 Automatic token refresh and management
- 📈 Portfolio analysis and visualization
- 🛡️ Secure credential management with environment variables

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
- Schwab Developer Account and API credentials
- Git (for version control)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd portfolio-analysis-app
```

### 2. Create Virtual Environment (Recommended)
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

1. **Create a Schwab Developer Account:**
   - Visit [https://developer.schwab.com/](https://developer.schwab.com/)
   - Click "Register" and create an account
   - Verify your email address

2. **Create an Application:**
   - Log in to the Developer Portal
   - Navigate to "My Apps"
   - Click "Create New App"
   - Fill in the application details:
     - **App Name:** Your application name (e.g., "Portfolio Analyzer")
     - **Redirect URI:** `https://127.0.0.1:5000/callback` (for local development)
     - **Description:** Brief description of your app

3. **Get Your Credentials:**
   - After creating the app, you'll receive:
     - **App Key** (Client ID)
     - **App Secret** (Client Secret)
   - Keep these secure and never commit them to version control!

### 5. Configure Environment Variables

1. **Copy the example environment file:**
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. **Edit the `.env` file** with your actual credentials:
   ```env
   SCHWAB_API_KEY=your_actual_app_key_here
   SCHWAB_API_SECRET=your_actual_app_secret_here
   SCHWAB_REDIRECT_URI=https://127.0.0.1:5000/callback
   
   FLASK_SECRET_KEY=your_generated_secret_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   FLASK_HOST=127.0.0.1
   FLASK_PORT=5000
   ```

3. **Generate a Flask secret key:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and paste it as your `FLASK_SECRET_KEY` in the `.env` file.

### 6. Test the Schwab API Connection

Before running the full application, test your API setup:

```bash
python test_schwab_connection.py
```

This script will:
- ✅ Validate your configuration
- ✅ Initialize the Schwab API client
- ✅ Guide you through OAuth authentication
- ✅ Test API connectivity
- ✅ Display available scopes/permissions
- ✅ Retrieve basic account information

**First-time authentication:**
- The script will open your browser automatically
- Log in to your Schwab account
- Authorize the application
- You'll be redirected to your redirect URI with an authorization code
- Copy the code from the URL and paste it into the terminal
- Your tokens will be saved for future use

### 7. Run the Application

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000`

## Configuration

### Environment Variables

All sensitive configuration is managed through environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SCHWAB_API_KEY` | Your Schwab App Key (Client ID) | Yes | - |
| `SCHWAB_API_SECRET` | Your Schwab App Secret | Yes | - |
| `SCHWAB_REDIRECT_URI` | OAuth redirect URI | Yes | `https://127.0.0.1:5000/callback` |
| `FLASK_SECRET_KEY` | Flask session secret | Yes | Auto-generated in dev |
| `FLASK_ENV` | Environment (development/production) | No | `development` |
| `FLASK_DEBUG` | Enable debug mode | No | `True` |
| `FLASK_HOST` | Server host | No | `127.0.0.1` |
| `FLASK_PORT` | Server port | No | `5000` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

### Security Best Practices

1. **Never commit sensitive files:**
   - `.env` file (contains credentials)
   - `schwab_tokens.json` (contains access tokens)
   - These are already in `.gitignore`

2. **Use HTTPS in production:**
   - Update `SCHWAB_REDIRECT_URI` to use HTTPS
   - Configure SSL certificates

3. **Rotate credentials regularly:**
   - Generate new App Keys periodically
   - Update `.env` file with new credentials

4. **Use strong secret keys:**
   - Generate cryptographically secure random keys
   - Never use default or example keys in production

## API Usage

### SchwabClient Methods

```python
from api.schwab_client import SchwabClient
from config import Config

# Initialize client
client = SchwabClient(
    api_key=Config.SCHWAB_API_KEY,
    api_secret=Config.SCHWAB_API_SECRET,
    redirect_uri=Config.SCHWAB_REDIRECT_URI
)

# Authenticate (handles OAuth flow)
client.authenticate()

# Get account numbers
accounts = client.get_account_numbers()

# Get account data with positions
account_data = client.get_account_data(fields="positions")

# Get portfolio data (convenience method)
portfolio = client.get_portfolio_data()

# Test connectivity and print status
client.print_connection_status()
```

### Error Handling

```python
from api.schwab_client import SchwabAPIError

try:
    client.authenticate()
    data = client.get_portfolio_data()
except SchwabAPIError as e:
    print(f"API Error: {e}")
```

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

## Troubleshooting

### Common Issues

**Issue: "Configuration validation failed"**
- **Solution:** Ensure all required environment variables are set in `.env`
- Run: `python -c "from config import Config; Config.print_config_status()"`

**Issue: "Token exchange failed"**
- **Solution:** Verify your API credentials are correct
- Ensure the redirect URI in `.env` matches the one in your Schwab app settings
- Check that you copied the authorization code correctly

**Issue: "Rate limit exceeded"**
- **Solution:** Schwab API has rate limits. Wait before retrying.
- Implement caching to reduce API calls

**Issue: "API access test failed"**
- **Solution:** Ensure your Schwab app has the required permissions
- Check that your account is approved for API access

**Issue: Import errors for `dotenv`**
- **Solution:** Install dependencies: `pip install -r requirements.txt`

### Getting Help

1. Check the [Schwab Developer Documentation](https://developer.schwab.com/)
2. Review the application logs
3. Use the test script for diagnostics: `python test_schwab_connection.py`

## API Rate Limits

Schwab API has rate limits:
- Be mindful of request frequency
- Implement caching where appropriate
- Handle 429 (rate limit) errors gracefully

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Write unit tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer

This application is for educational and personal use only. Always ensure compliance with:
- Schwab's Terms of Service
- API usage guidelines
- Financial data privacy regulations

**Important:** Never share your API credentials or access tokens. Keep all sensitive information secure.

## Acknowledgments

- [Schwab Developer Platform](https://developer.schwab.com/) for providing API access
- Flask framework and its community
- All contributors to this project

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the Schwab Developer documentation

---

**Happy Analyzing! 📊💼**