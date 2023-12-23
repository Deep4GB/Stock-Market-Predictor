import yfinance as yf
from newsapi import NewsApiClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests

# Initialize NewsAPI client and Sentiment Analyzer
newsapi = NewsApiClient(api_key='f559e09d793245729d4affef1d073f15')  # Replace with your NewsAPI key
sia = SentimentIntensityAnalyzer()

def get_stock_news(ticker):
    try:
        # Get stock information
        stock = yf.Ticker(ticker)
        stock_info = stock.info

        # Get the latest news headlines related to the stock
        headlines = newsapi.get_everything(q=stock_info['shortName'],
                                           language='en',
                                           sort_by='publishedAt',
                                           page_size=5)

        if headlines['status'] == 'ok' and headlines['totalResults'] > 0:
            articles = headlines['articles']

            # Analyze sentiment of news headlines
            positive_count = 0
            negative_count = 0

            for article in articles:
                headline = article['title']
                sentiment_score = sia.polarity_scores(headline)['compound']

                if sentiment_score > 0:
                    positive_count += 1
                elif sentiment_score < 0:
                    negative_count += 1

                print(f"Headline: {headline}")
                print(f"Sentiment: {'Positive' if sentiment_score > 0 else 'Negative'}")
                print("-" * 50)

            # Determine overall sentiment based on news
            if positive_count > negative_count:
                print("Overall sentiment: Positive")
            elif positive_count < negative_count:
                print("Overall sentiment: Negative")
            else:
                print("Overall sentiment: Neutral")
        else:
            print("No news found for this stock.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except ValueError as e:
        print(f"Value error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    ticker_symbol = input("Enter the stock ticker symbol: ")
    get_stock_news(ticker_symbol)
