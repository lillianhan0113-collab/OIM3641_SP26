import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Stock:
    def __init__(self, symbol, start_date=None, end_date=None):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def get_data(self):
        if self.end_date is None:
            self.end_date = datetime.today().strftime('%Y-%m-%d')

        if self.start_date is None:
            last_year = datetime.today() - timedelta(days=365)
            self.start_date = last_year.strftime('%Y-%m-%d')

        df = yf.download(
            self.symbol,
            start=self.start_date,
            end=self.end_date,
            interval="1d",
            auto_adjust=True
        )

        df.index = pd.to_datetime(df.index)
        self.data = df
        self.calc_returns()

    def calc_returns(self):
        self.data["change"] = self.data["Close"].diff()
        self.data["instant_return"] = np.log(self.data["Close"]).diff().round(4)

    def add_technical_indicators(self):

        self.data["MA20"] = self.data["Close"].rolling(20).mean()
        self.data["MA50"] = self.data["Close"].rolling(50).mean()

        plt.figure(figsize=(10,5))
        plt.plot(self.data["Close"], label="Close")
        plt.plot(self.data["MA20"], label="MA20")
        plt.plot(self.data["MA50"], label="MA50")

        plt.title("Price with Moving Averages")
        plt.legend()
        plt.show()

    def plot_return_dist(self):

        plt.figure(figsize=(8,4))
        plt.hist(self.data["instant_return"].dropna(), bins=50)

        plt.title("Instantaneous Return Distribution")
        plt.xlabel("Return")
        plt.ylabel("Frequency")
        plt.show()

    def plot_performance(self):

        first_price = self.data["Close"].iloc[0]
        performance = (self.data["Close"] / first_price - 1) * 100

        plt.figure(figsize=(10,5))
        plt.plot(performance)

        plt.title("Stock Performance (%)")
        plt.xlabel("Date")
        plt.ylabel("Percent Gain/Loss")
        plt.show()

if __name__ == "__main__":
    test = Stock("AAPL")
    test.get_data()

    print(test.data.head())

    test.add_technical_indicators()
    test.plot_return_dist()
    test.plot_performance()