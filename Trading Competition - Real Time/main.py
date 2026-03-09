import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
import datetime
from datetime import datetime, time as dt_time
import time
from data_loader import data_loader
from engine import Engine
from reporting import report
import numpy as np
import pandas as pd
import alpaca_trade_api as tradeapi
from multiprocessing import Process
from alpaca.trading.client import TradingClient
from alpaca_trade_api.rest import TimeFrame
from alpaca.data.requests import StockLatestBarRequest
from alpaca.data import StockHistoricalDataClient

api = tradeapi.REST('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi', 'https://paper-api.alpaca.markets')
client = StockHistoricalDataClient('PKA2YLOYQMRLU4UXQGWFFENIVE', 'GDn1KmHfKLQJBDWv1YiEecccgnH35qa7TwwiuRAa1HKi')

timeframe = '1Min'
start_date = "2026-03-01"
end_date = "2026-03-06"

symbol = 'AAPL'
file_path = 'market_data_AAPL.csv'
risk = 10000
stop = 0.03
bar_data = client.get_stock_latest_bar(StockLatestBarRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute))[symbol]
market_sample = pd.DataFrame({
    'timestamp': [bar_data.timestamp],
    'open': [bar_data.open],
    'high': [bar_data.high],
    'low': [bar_data.low],
    'close': [bar_data.close],
    'volume': [bar_data.volume]
})

def main(symbol):
    start_time = dt_time(9, 30)
    end_time = dt_time(16, 0)
    result = np.empty((0, 4))
    market_data = pd.DataFrame(columns=market_sample.columns).astype(market_sample.dtypes)
    request_params = StockLatestBarRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute)

    while True:
        now = datetime.now().time()
        if start_time <= now < end_time:

            capital = api.get_account().cash
            latest_bar = client.get_stock_latest_bar(request_params)[symbol]
            data = pd.DataFrame({'timestamp': [latest_bar.timestamp],
                                 'open': [latest_bar.open],
                                 'high': [latest_bar.high],
                                 'low': [latest_bar.low],
                                 'close': [latest_bar.close],
                                 'volume': [latest_bar.volume]})
            market_data = pd.concat([market_data, data], axis=0, ignore_index=True)
            new_result = Engine(risk, stop, market_data[['high', 'low', 'close']], capital, symbol).execute().reshape(1,-1)
            result = np.append(result, new_result, axis=0)
            report(market_data[['timestamp', 'close']], result, symbol)
            print(rf'[LOG] {now} - Running {symbol} trade finished.')
            time.sleep(60)
        else:
            print(rf"Outside working hours, sleeping... {now}")
            time.sleep(3600)

if __name__ == '__main__':
    p1 = Process(target=main, args=('AAPL',))
    p2 = Process(target=main, args=('MSFT',))
    p3 = Process(target=main, args=('TSLA',))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()