from flask import Flask, render_template, request
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to build and compile the LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Route to display the input form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.form['ticker']

    # Download data from Yahoo Finance
    data = yf.download(ticker, start='2000-01-01')

    # Save the downloaded data as a CSV file
    data.to_csv(f"{ticker}_stock_data.csv", index=False)

    # Extract the 'Close' prices
    df = data[['Close']]
    df.reset_index(inplace=True)

    # Convert date to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Set today's date
    today = datetime(2023, 11, 6)

    # Filter to only data before today
    df = df[df['Date'] < today]

    # Extract 'Close' prices
    close_prices = df['Close'].values

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    close_prices = scaler.fit_transform(close_prices.reshape(-1, 1))

    # Prepare the data for training
    X, y = [], []
    look_back = 60  # Number of previous time steps to use for prediction

    for i in range(len(close_prices) - look_back):
        X.append(close_prices[i:i+look_back])
        y.append(close_prices[i+look_back])

    X, y = np.array(X), np.array(y)

    # Split data into training and testing sets
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Build and compile the LSTM model
    input_shape = (look_back, 1)
    model = build_lstm_model(input_shape)

    # Train the model for a reduced number of epochs (e.g., 10)
    model.fit(X_train, y_train, batch_size=64, epochs=10)

    # Predict the next day's stock price
    inputs = close_prices[-look_back:]
    X_new = np.array([inputs])
    X_new = np.reshape(X_new, (X_new.shape[0], X_new.shape[1], 1))
    predicted_price = model.predict(X_new)
    predicted_price = scaler.inverse_transform(predicted_price)

    # Print the predicted price
    tomorrow = today + timedelta(days=1)
    print(f"Predicted close price for {ticker} on {tomorrow}: {predicted_price[0][0]:.2f}")

    return render_template('result.html', ticker=ticker, predicted_price=predicted_price)


if __name__ == '__main__':
    app.run(debug=True)