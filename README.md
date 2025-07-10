# currency-tracker
Real-time currency tracker with forex news, trends and forecasts using ARIMA model 📈

A Streamlit-based web application for tracking real-time currency exchange rates, forecasting future rates using the ARIMA model, and staying updated with the latest forex news. This application provides a sleek, user-friendly interface with dark/light mode support, interactive charts, and downloadable data.
Table of Contents

Features
Demo
Installation
Usage
API Dependencies
File Structure
Technologies Used
Contributing
License
Contact

Features

Real-Time Currency Conversion: Convert amounts between a base currency and up to 5 target currencies using real-time exchange rates from the Frankfurter API.
Historical Trends: Visualize exchange rate trends over a customizable time period (1 to 3650 days).
ARIMA Forecasting: Predict future exchange rates using the ARIMA model with confidence intervals.
Forex News Feed: Stay updated with the latest forex news fetched via the NewsAPI.
Alert System: Set thresholds to receive alerts when exchange rates exceed specified values.
Dark/Light Mode: Toggle between dark and light themes for better readability.
Downloadable Data: Export historical data and forecasts as CSV files or charts as PNG images.
Volatility Metrics: View annualized volatility based on daily returns for selected currencies.
Interactive UI: Built with Streamlit and Plotly for a seamless and visually appealing experience.

Demo
A live demo is not currently hosted, but you can run the application locally by following the Installation and Usage instructions below. Here's a preview of what the app looks like:

Installation
Follow these steps to set up the project locally:

Clone the Repository:
git clone https://github.com/yourusername/pro-currency-tracker.git
cd pro-currency-tracker


Set Up a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:Ensure you have Python 3.8+ installed. Then, install the required packages:
pip install -r requirements.txt


Create a requirements.txt File:If not already present, create a requirements.txt file with the following content:
streamlit==1.38.0
requests==2.32.3
pandas==2.2.2
plotly==5.24.1
statsmodels==0.14.3


Obtain a NewsAPI Key:

Sign up at NewsAPI to get a free API key.
Replace the NEWS_API_KEY in main.py with your API key:NEWS_API_KEY = "your-api-key-here"




Run the Application:
streamlit run main.py

The app will open in your default browser at http://localhost:8501.


Usage

Select Base Currency and Amount:

Enter a valid 3-letter currency code (e.g., USD) and the amount to convert in the sidebar.
The app validates the currency code using the Frankfurter API's currency list.


Choose Target Currencies:

Select up to 5 target currencies from the dropdown menus.
Each currency is displayed with its full name and flag emoji for clarity.


Set Time Range:

Use the slider to select the number of days (1 to 3650) for historical exchange rate trends.


Configure Alerts:

Set optional alert thresholds for each target currency to receive warnings if rates exceed the specified value.


View Results:

The app displays the converted amounts, historical trends (via Plotly charts), and forecasted rates using the ARIMA model.
Download historical data as CSV or charts as PNG using the provided buttons.


Explore Forex News:

The latest forex-related news articles are displayed in a grid, with links to full articles.


Analyze Volatility:

Check the annualized volatility for each target currency based on daily returns.


Toggle Theme:

Switch between dark and light modes using the sidebar button for a personalized experience.



API Dependencies

Frankfurter API: Provides real-time and historical exchange rate data. No API key is required.
Endpoint: https://api.frankfurter.app/


NewsAPI: Fetches forex-related news articles. Requires an API key.
Endpoint: https://newsapi.org/v2/everything
Note: The free NewsAPI plan has limitations (e.g., 100 requests/day). Ensure your key is valid.



File Structure
pro-currency-tracker/
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── assets/              # (Optional) Folder for images, GIFs, or other media

Technologies Used

Python 3.8+: Core programming language.
Streamlit: Framework for building the web application.
Pandas: Data manipulation and analysis.
Plotly: Interactive charting and visualization.
Statsmodels: ARIMA model for forecasting.
Requests: HTTP requests for API calls.
CSS: Custom styling for the Streamlit interface.
HTML: Embedded in Streamlit for news cards and styling.

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

Please ensure your code follows PEP 8 guidelines and includes appropriate comments.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact

Author: Yeaomun Tousif
Email: your.email@example.com
GitHub: yourusername

For issues or feature requests, please open an issue on the GitHub repository.

Made with ❤️ by Yeaomun Tousif — Empowering you to track and forecast currencies with ease!
