import pprint

import yfinance as yf


def get_market_price(symbol: str):

    if symbol == "tbd":
        return 0.0
    symbol = symbol + ".DE"
    data = yf.Ticker(symbol).info
    test = data["regularMarketPreviousClose"]
    return test
