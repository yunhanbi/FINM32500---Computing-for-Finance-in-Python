import alpaca_trade_api as tradeapi
from alpaca.trading.client import TradingClient

api = tradeapi.REST('PK6ICUILQVKXFEDM7IYXEEQLRY', '7CB8dzqytZqK7zrJZwDpaH6YCBaRYWFdvE5aFx1Qtf45', 'https://paper-api.alpaca.markets')

symbol = "AAPL"
timeframe = '1Min'
start_date = "2026-03-01"
end_date = "2026-03-06"

data = api.get_bars(symbol, timeframe, start=start_date, end=end_date).df.reset_index(drop=False).iloc[[-1], :]

print(data.dtypes)
print(api.get_account().cash)

