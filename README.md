<h2 align="center"> ━━━━━━  ❖  ━━━━━━ </h2>
<h1 align="center"> Stock Price Prediction Using ML </h1>

## Table of Contents
- [Project Overview](#project-overview)
- [Access Full Report](#access-full-report)
- [Instructions to Run](#instructions-to-run)
- [Deep Learning (LSTM)](#deep-learning-lstm)
- [Machine Learning (Random Forest Regressor)](#machine-learning-random-forest-regressor)
- [Streamlit Based Application](#streamlit-based-application)
- [Contribute](#contribute)

## Project Overview
The Stock Price Predictor project offers an accessible and intuitive interface for stock price prediction and analysis. This project employs two distinct methodologies: Jupyter Notebooks and a Streamlit-based application that utilizes machine learning techniques.

## Access Full Report
If you want to access the detailed report and code implementations, you can view it [Stock Price Prediction report](https://stock-prediction-report.deeppatel.tech/#62cf0ed2-6749-4e80-b71e-6487f9036bd9). The full report contains comprehensive details, code explanations, and insights from the analysis.

## Instructions to Run
1. **Clone the repository:**
    ```bash
    gh repo clone Deep4GB/Stock-Market-Predictor
    ```
2. **Install Dependencies:**
    ```bash 
    pip install -r requirements.txt
    ```
3. **Run the Application (Streamlit):**
    ```bash 
    streamlit run stock_predictor.py
    ```

## Deep Learning (LSTM)
The `deep_learning.ipynb` notebook implements a Long Short-Term Memory (LSTM) neural network for stock price prediction. This notebook provides an in-depth exploration of the LSTM model's performance and its ability to predict stock prices effectively.

## Machine Learning (Random Forest Regressor)
In the `machine_learning.ipynb` notebook, a Random Forest Regressor machine learning technique is employed to forecast stock prices. This notebook serves as a comparative analysis against the LSTM model, examining the Random Forest Regressor's performance in predicting stock prices.

## Streamlit Based Application
The `stock_predictor.py` script fetches historical stock data from Yahoo Finance, conducts data preprocessing such as calculating Moving Averages (MA), and trains the Random Forest Regressor model. The Streamlit-based user interface enables users to input a stock symbol, specify date ranges, and visualize predictions along with other significant stock market indicators.

### Detailed Functionality
- Fetches historical stock data from Yahoo Finance.
- Preprocesses data including calculating Moving Averages (MA).
- Trains a Random Forest Regressor model for stock price prediction.
- Provides an interactive UI for users to input stock details and visualize predictions.

## Contribute
Contributions are welcome! Feel free to contribute by opening issues, suggesting improvements, or creating pull requests. We aim to make this project informative and useful for exploring stock price prediction. Your input is appreciated.

<h3 align="center"> ━━━━━━ End of Document ━━━━━━ </h3>
