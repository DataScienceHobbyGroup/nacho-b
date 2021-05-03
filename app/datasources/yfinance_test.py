import yfinance as yf
msft = yf.Ticker("NANO-USD")
print(msft.info)