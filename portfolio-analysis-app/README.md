# Portfolio Analysis App

## Overview
The Portfolio Analysis App is a Flask-based web application designed to analyze and visualize investment portfolios using data retrieved from the Schwab developer APIs. This application provides a user-friendly interface for users to input their portfolio details and receive insights based on their investments.

## Project Structure
```
portfolio-analysis-app
├── app.py                # Entry point of the Flask application
├── config.py             # Configuration settings for the application
├── requirements.txt      # List of dependencies
├── static                # Static files (CSS, JS)
│   ├── css
│   │   └── style.css     # Styles for the frontend
│   └── js
│       └── app.js        # JavaScript for frontend interactions
├── templates             # HTML templates
│   └── index.html        # Main HTML template
├── api                   # API related files
│   ├── __init__.py       # Initializes the API package
│   ├── routes.py         # Defines API routes
│   └── schwab_client.py  # Client for Schwab API communication
├── helpers               # Helper functions and classes
│   ├── __init__.py       # Initializes the helpers package
│   ├── portfolio_analyzer.py # Functions for portfolio analysis
│   └── data_processor.py  # Functions for data processing
└── README.md             # Project documentation
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd portfolio-analysis-app
   ```

2. **Install dependencies:**
   Ensure you have Python and pip installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   Update the `config.py` file with your Schwab API keys and any other necessary configuration settings.

4. **Run the application:**
   Start the Flask application by executing:
   ```
   python app.py
   ```
   The application will be accessible at `http://127.0.0.1:5000`.

## Usage
- Navigate to the homepage to input your portfolio details.
- The application will analyze the data and provide insights based on the Schwab APIs.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.