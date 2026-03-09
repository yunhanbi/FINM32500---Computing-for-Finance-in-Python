import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.requests import StockLatestBarRequest
from alpaca.data import StockHistoricalDataClient
import pandas as pd

api = tradeapi.REST('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi', 'https://paper-api.alpaca.markets')
# trading_client = TradingClient('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi', paper=True)

symbol = "AAPL"
timeframe = '1Min'
start_date = "2026-03-01"
end_date = "2026-03-06"

trading_client = TradingClient('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi', paper=True)

client = StockHistoricalDataClient('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi')

# Define the symbol
symbol = "AAPL"

# Create the request object for the latest 1-min bar
request_params = StockLatestBarRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute)

# Retrieve the data
latest_bar = client.get_stock_latest_bar(request_params)

# print(client.get_stock_latest_bar(StockLatestBarRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute))[symbol])
# final_order = MarketOrderRequest(
#     symbol='AAPL',
#     qty=3,
#     side=OrderSide.SELL,
#     time_in_force=TimeInForce.GTC
# )
# trading_client.submit_order(final_order)
# print(pd.DataFrame(client.get_stock_latest_bar(StockLatestBarRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute))[symbol]))

# print(api.get_bars("TSLA", "1Min").df.reset_index(drop=False))
bar_data = latest_bar["AAPL"]
print(pd.DataFrame({
    'timestamp': [bar_data.timestamp],
    'open': [bar_data.open],
    'high': [bar_data.high],
    'low': [bar_data.low],
    'close': [bar_data.close],
    'volume': [bar_data.volume]
}))