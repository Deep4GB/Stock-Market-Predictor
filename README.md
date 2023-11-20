# Stock Price Predictor

## Project Overview
The Stock Price Predictor project offers a user-friendly interface for stock price prediction and analysis. It employs two distinct methodologies represented by Jupyter Notebooks and a Streamlit-based application utilizing machine learning techniques.


# 

# Instructions to run

1. Clone the repository:
```bash
gh repo clone Deep4GB/Stock-Market-Predictor
```
2. Install Dependencies: Execute the following command to install all required libraries:
```bash 
pip install -r requirements.txt
```
3. Run the Application (Streamlit):
```bash 
streamlit run stock_predictor.py
```
4. Jupyter Notebook Usage:
- Open and execute the Jupyter Notebooks (deep_learning.ipynb and machine_learning.ipynb) step by step or run all cells.

#

### **Deep Learning (LSTM)**:
The deep_learning.ipynb notebook utilizes a Long Short-Term Memory (LSTM) neural network for stock price prediction. This notebook provides an in-depth exploration of the LSTM model's performance and its ability to predict stock prices effectively.
#
### **Machine Learning (Random Forest Regressor)**:
In the machine_learning.ipynb notebook, a Random Forest Regressor, a machine learning technique, is utilized to predict stock prices. This notebook serves as a comparative analysis against the LSTM model, examining the Random Forest Regressor's performance in forecasting stock prices.

# 
### **Streamlit based application**:
The stock_predictor.py script fetches historical stock data from Yahoo Finance, performs data preprocessing tasks like calculating Moving Averages (MA), and trains the Random Forest Regressor model. The Streamlit-based user interface enables users to input a stock symbol, specify date ranges, and visualize predictions along with other significant stock market indicators.

# 
## Contribute

Feel free to contribute to the project by opening issues, suggesting improvements, or creating pull requests. We hope you find this project informative and useful for exploring stock price prediction. Enjoy the visualizations!

Team - Deep, Dravya, Sahil
