import requests
from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
import plotly.graph_objects as go

app = Flask(__name__)

# Suppress the specific warning
warnings.filterwarnings("ignore", category=UserWarning)


# Function to fetch historical stock data from Yahoo Finance
def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of an error


# Function to calculate Moving Average (MA) for a given window
def calculate_moving_average(data, window):
    return data['Close'].rolling(window=window).mean()

# Function to add Moving Average as a feature to the dataset


def add_moving_average_feature(data, window):
    data['MA'] = calculate_moving_average(data, window)
    return data

# Function to preprocess data for training the model


def preprocess_data(data, ma_window):
    data = add_moving_average_feature(data, ma_window)
    data['Date'] = data.index
    data['Date'] = pd.to_datetime(
        data['Date']).dt.date.apply(lambda x: x.toordinal())

    # Explicitly include the 'Close' column
    data['Close'] = data['Close']

    # Fill NaN values with 0
    data = data.fillna(0)

    return data

# Function to train a Random Forest Regressor model


def train_model(data):
    X = data[['Date', 'Open', 'High', 'Low', 'Volume', 'MA']]
    y = data['Close']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, X_test, y_test, scaler

# Function to predict the next day's closing price


def predict_price(model, last_date, scaler, open_price, high_price, low_price, volume):
    next_date = last_date + timedelta(days=1)
    next_date_ordinal = next_date.toordinal()
    # 0 is a placeholder for MA since it's not available for the next day
    input_data = np.array(
        [[next_date_ordinal, open_price, high_price, low_price, volume, 0]])
    input_data_scaled = scaler.transform(input_data)
    return model.predict(input_data_scaled)[0]

# Flask routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stock')
def stock():
    return render_template('stock.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/get_stock_price', methods=['POST'])
def get_stock_price():
    ticker_symbol = request.form['tickerSymbol']
    stock = yf.Ticker(ticker_symbol)

    try:
        price_data = stock.history(period='1d')
        if not price_data.empty:
            # Get the latest closing price
            current_price = price_data['Close'].iloc[-1]
            return {'currentPrice': str(current_price)}
        else:
            return {'currentPrice': 'Failed to fetch current price'}
    except Exception as e:
        print(f"Error fetching stock price: {e}")
        return {'currentPrice': 'Failed to fetch current price'}


@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')


@app.route('/predict', methods=['GET', 'POST'])
def prediction():
    prediction_text = ""  # Define an initial value for prediction_text
    chart_data = None  # Define an initial value for chart_data

    if request.method == 'POST':
        # Handle form submission here
        # Fetch form data
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        ma_window = request.form['ma_window']

        # Fetch historical stock data
        stock_data = get_stock_data(symbol, start_date, end_date)

        if stock_data.empty:
            prediction_text = "No data found for the given symbol and date range"
        else:
            # Preprocess data
            processed_data = preprocess_data(stock_data, int(ma_window))

            if len(processed_data) > 0:  # Check if processed_data contains samples
                try:
                    # Train the model
                    model, X_test, y_test, scaler = train_model(processed_data)

                    # Get the latest data for prediction
                    latest_data = processed_data.iloc[-1]
                    open_price = latest_data['Open']
                    high_price = latest_data['High']
                    low_price = latest_data['Low']
                    volume = latest_data['Volume']

                    # Predict the next day's closing price
                    next_price = predict_price(
                        model, latest_data.name, scaler, open_price, high_price, low_price, volume)

                    # Update prediction_text with the predicted price
                    prediction_text = f"Predicted closing price: ${next_price:.2f}"

                    # Example: Generate chart data for visualization
                    # Replace with actual chart data based on your requirements
                    # Replace with actual chart data
                    chart_data = {"x": [1, 2, 3], "y": [10, 20, 30]}

                except Exception as e:
                    print(f"Error during prediction: {e}")
                    prediction_text = "Error occurred during prediction"
            else:
                prediction_text = "Insufficient data for prediction"
                symbol = request.args.get('symbol')
                current_price = request.args.get('price')

    return render_template('prediction.html', symbol=symbol, prediction_text=prediction_text, chart_data=chart_data)


if __name__ == '__main__':
    app.run(debug=True)
