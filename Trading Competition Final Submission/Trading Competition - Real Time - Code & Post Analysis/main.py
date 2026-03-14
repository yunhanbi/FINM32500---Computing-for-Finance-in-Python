import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
import datetime
from datetime import datetime, time as dt_time
import time
import os
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

api = tradeapi.REST('PK6ICUILQVKXFEDM7IYXEEQLRY', '7CB8dzqytZqK7zrJZwDpaH6YCBaRYWFdvE5aFx1Qtf45', 'https://paper-api.alpaca.markets')
client = StockHistoricalDataClient('PK6ICUILQVKXFEDM7IYXEEQLRY', '7CB8dzqytZqK7zrJZwDpaH6YCBaRYWFdvE5aFx1Qtf45')
trading_client = TradingClient("PK6ICUILQVKXFEDM7IYXEEQLRY", "7CB8dzqytZqK7zrJZwDpaH6YCBaRYWFdvE5aFx1Qtf45", paper=True)

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
all_symbols = [position.symbol for position in trading_client.get_all_positions()]

def main(symbol):
    start_time = dt_time(6, 30)
    end_time = dt_time(16, 00)
    result = np.empty((0, 6))
    market_data = pd.DataFrame(columns=market_sample.columns).astype(market_sample.dtypes)
    request_params = StockLatestBarRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute)
    position = 0
    avg_price = 0
    if os.path.isfile(f'final_report_{symbol}.csv'):
        result = pd.read_csv(f'final_report_{symbol}.csv').to_numpy()
        avg_price = result[-1,1]
    if symbol in all_symbols:
        position = trading_client.get_open_position(symbol).qty

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
            new_result = Engine(risk, stop, market_data[['high', 'low', 'close']], capital, symbol, position, avg_price).execute().reshape(1,-1)
            result = np.append(result, np.hstack((new_result, np.array(data[['timestamp', 'close']]))), axis=0)
            report(result, symbol)
            print(rf'[LOG] {now} - Running {symbol} trade finished.')
            time.sleep(60)
        else:
            print(rf"Outside working hours, sleeping... {now}")
            time.sleep(3600)

if __name__ == '__main__':
    p1 = Process(target=main, args=('INTC',))
    p2 = Process(target=main, args=('NVDA',))
    p3 = Process(target=main, args=('AMD',))

    p1.start()
    time.sleep(3)
    p2.start()
    time.sleep(4)
    p3.start()

    p1.join()
    p2.join()
    p3.join()