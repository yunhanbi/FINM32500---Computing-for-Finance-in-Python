import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
from models import ExecutionError, Order
from strategies import MomentumStrategy, MovingAverageCrossoverStrategy, Strategy
import numpy as np
from data_loader import data_loader
import pandas as pd
import threading
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import traceback

thread_storage = threading.local()

class Engine(MomentumStrategy, MovingAverageCrossoverStrategy):
    def __init__(self, risk, stop, market_data, capital, symbol, qty, avg_price):
        super().__init__(risk, stop)
        self.__market_data = market_data
        self.symbol = symbol
        self._capital = float(capital)
        self.__position = thread_storage.position if hasattr(thread_storage, 'position') else {self.symbol: {'quantity': int(qty), 'avg_price': float(avg_price)}}

    @property
    def risk(self):
        return self._risk

    @risk.setter
    def risk(self, override):
        self._risk = override

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, override):
        self._stop = override

    def execute(self):
        try:
            trading_client = TradingClient('PK6ICUILQVKXFEDM7IYXEEQLRY', '7CB8dzqytZqK7zrJZwDpaH6YCBaRYWFdvE5aFx1Qtf45', paper=True)
            actions = []
            self._risk = self._capital * 0.15
            MM_action = MomentumStrategy.generate_signals(self, self.__market_data, self.__position[self.symbol]['quantity'], self.__position[self.symbol]['avg_price'], self.symbol)
            MAC_action = MovingAverageCrossoverStrategy.generate_signals(self, self.__market_data, self.__position[self.symbol]['quantity'], self.__position[self.symbol]['avg_price'], self.symbol)
            if MM_action[0] != 'pass' or MAC_action[0] != 'pass':
                final_qty = ((MM_action[2] if MM_action[0] == 'buy' else -MM_action[2]) + (MAC_action[2] if MAC_action[0] == 'buy' else -MAC_action[2])) // 2
                action = ('buy' if final_qty > 0 else 'sell', self.symbol, abs(final_qty), self.__market_data.close.iloc[-1])
                if action[2] > 0:
                    final_order = MarketOrderRequest(
                        symbol=str(action[1]),
                        qty=int(action[2]),
                        side=OrderSide.BUY if action[0] == 'buy' else OrderSide.SELL,
                        time_in_force=TimeInForce.GTC
                    )
                    trading_client.submit_order(final_order)
            else:
                action = ('pass', self.symbol, 0, self.__market_data.close.iloc[-1])
            order = Order(action[0], action[1], action[2], action[3])
            update = order.update_portfolio(self.__position)
            if self._capital > 0:
                self._capital += update[1]
            if type(update) is list:
                self.__position = update[0]
                actions.append(action)

            thread_storage.position = self.__position
            return np.hstack((np.array([self.__position[self.symbol]['quantity'], self.__position[self.symbol]['avg_price']]), np.array([update[1]]), np.array([self._capital])))
        except Exception as e:
            print(e)
            print(traceback.print_exc())
            return e