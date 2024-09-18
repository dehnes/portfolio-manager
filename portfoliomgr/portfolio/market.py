import pprint

import yfinance as yf


def get_market_price(symbol: str = "tbd") -> float:

    if symbol == "tbd":
        return 0.0
    symbol += ".DE"
    data = yf.Ticker(symbol).fast_info
    result = float(data["regularMarketPreviousClose"])
    return result
