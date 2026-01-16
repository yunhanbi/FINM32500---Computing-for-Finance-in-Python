import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
from models import ExecutionError, Order
from strategies import MomentumStrategy, MovingAverageCrossoverStrategy, Strategy
import numpy as np
from data_loader import data_loader
import pandas as pd

class Engine(MomentumStrategy, MovingAverageCrossoverStrategy):
    def __init__(self, risk, stop, market_data, capital):
        super().__init__(risk, stop)
        self.__market_data = market_data
        self._capital = capital
        self.__position = {'AAPL': {'quantity': 0, 'avg_price': 0.0}}
        self._position_hist = np.empty((0,2))
        self.__return_hist = []
        self.__capital_hist = []

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
            actions = []
            for datapoint in self.__market_data:
                MM_action = MomentumStrategy.generate_signals(self, datapoint, self.__position[datapoint.symbol]['quantity'], self.__position[datapoint.symbol]['avg_price'])
                MAC_action = MovingAverageCrossoverStrategy.generate_signals(self, datapoint, self.__position[datapoint.symbol]['quantity'], self.__position[datapoint.symbol]['avg_price'])
                if MM_action[0] != 'pass' or MAC_action[0] != 'pass':
                    final_qty = ((MM_action[2] if MM_action[0] == 'buy' else -MM_action[2]) + (MAC_action[2] if MAC_action[0] == 'buy' else -MAC_action[2])) // 2
                    action = ('buy' if final_qty > 0 else 'sell', datapoint.symbol, abs(final_qty), datapoint.price)
                else:
                    action = ('pass', datapoint.symbol, 0, datapoint.price)
                order = Order(action[0], action[1], action[2], action[3])
                update = order.update_portfolio(self.__position)

                if self._capital > 0:
                    self._capital += update[1]
                self._risk = self._capital * 0.15
                if type(update) is list:
                    self.__position = update[0]
                    self._position_hist = np.vstack((self._position_hist, [self.__position[datapoint.symbol]['quantity'], self.__position[datapoint.symbol]['avg_price']]))
                    self.__return_hist.append(update[1])
                    self.__capital_hist.append(self._capital)
                    actions.append(action)

            return np.hstack((self._position_hist, np.array(self.__return_hist).reshape(-1, 1), np.array(self.__capital_hist).reshape(-1, 1)))
        except Exception as e:
            return e