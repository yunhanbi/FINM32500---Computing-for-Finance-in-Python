import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.requests import StockLatestBarRequest
from alpaca.data import StockHistoricalDataClient

client = TradingClient('PK6ICUILQVKXFEDM7IYXEEQLRY', '7CB8dzqytZqK7zrJZwDpaH6YCBaRYWFdvE5aFx1Qtf45', paper=True)

# Get all open positions
print(client.get_all_positions())

