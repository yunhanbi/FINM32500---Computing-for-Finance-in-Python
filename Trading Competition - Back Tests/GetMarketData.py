import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

api = tradeapi.REST('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi', 'https://paper-api.alpaca.markets')
# trading_client = TradingClient('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi', paper=True)

symbol = "AAPL"
timeframe = '1Min'
start_date = "2026-03-01"
end_date = "2026-03-06"

trading_client = TradingClient('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi', paper=True)

final_order = MarketOrderRequest(
    symbol='AAPL',
    qty=3,
    side=OrderSide.SELL,
    time_in_force=TimeInForce.GTC
)
trading_client.submit_order(final_order)

print(api.get_bars("AAPL", "1Min", limit=1))