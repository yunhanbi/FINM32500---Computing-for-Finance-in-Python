import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
import numpy as np
from models import ExecutionError, Order
from data_loader import data_loader
import threading

thread_storage = threading.local()

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick) -> list:
        pass

class MomentumStrategy(Strategy):
    def __init__(self, risk: float, stop: float):
        super().__init__(risk, stop)
        self._period = 3
        self._adx_target = 25
        self._rsi_target = (40, 60)
        self._window = 30
        self.__adx = thread_storage.adx if hasattr(thread_storage, 'adx') else None
        self.__dm_pos = thread_storage.dm_pos if hasattr(thread_storage, 'dm_pos') else None
        self.__dm_neg = thread_storage.dm_neg if hasattr(thread_storage, 'dm_neg') else None
        self.__tr = thread_storage.tr if hasattr(thread_storage, 'tr') else None

    def generate_adx(self, vec):
        vec_max = vec[1:, 0]
        vec_min = vec[1:, 1]
        vec_cls = vec[:-1, 2]
        tr = np.max(np.vstack((vec_max - vec_min, vec_max - vec_cls, vec_min - vec_cls)), axis=0)
        dm_pos = np.maximum(np.diff(vec_max), 0)
        dm_neg = np.maximum(-np.diff(vec_min), 0)
        dm_diff = dm_pos > dm_neg
        dm_pos[~dm_diff] = 0
        dm_neg[dm_diff] = 0
        self.__dm_pos = np.mean(dm_pos) if self.__dm_pos is None else self.__dm_pos * (
                    1 - (1 / (self._window))) + np.mean(dm_pos) * (1 / self._window)
        self.__dm_neg = np.mean(dm_neg) if self.__dm_neg is None else self.__dm_neg * (
                    1 - (1 / (self._window))) + np.mean(dm_neg) * (1 / self._window)
        self.__tr = np.mean(tr) if self.__tr is None else self.__tr * (
                    1 - (1 / (self._window))) + np.mean(tr) * (1 / self._window)
        di_pos = (self.__dm_pos / self.__tr) * 100
        di_neg = (self.__dm_neg / self.__tr) * 100
        self.__adx = (abs(di_pos - di_neg) / (di_pos + di_neg)) * 100

        thread_storage.adx = self.__adx
        thread_storage.dm_pos = self.__dm_pos
        thread_storage.dm_neg = self.__dm_neg
        thread_storage.tr = self.__tr

        return [self.__adx, 'uptrend' if di_pos > di_neg else 'downtrend']

    def generate_rsi(self, vec):
        diff = np.diff(vec[-self._window:, 2])
        avg_gain = diff[diff > 0].mean()
        avg_loss = abs(diff[diff <= 0].mean())
        return 100 - (100 / (1 + (avg_gain / avg_loss)))

    def generate_signals(self, market_data, current_qty, avg_price, symbol) -> list:
        tick = market_data.iloc[-1,:]
        if len(market_data) < self._window:
            return ('pass', symbol, 0, float(tick.close))
        vec = market_data.iloc[-(self._window):, :].to_numpy()
        adx = self.generate_adx(vec)
        if adx[0] < self._adx_target:
            # print('Not a strong trend')
            return ('pass', symbol, 0, float(tick.close))
        elif adx[1] == 'uptrend' and self.generate_rsi(vec) < self._rsi_target[0]:
            return ('buy', symbol, int(self._risk // tick.close), float(tick.close))
        elif adx[1] == 'downtrend' and self.generate_rsi(vec) > self._rsi_target[1]:
            return ('sell', symbol, int(current_qty), float(tick.close))
        else:
            return ('pass', symbol, 0, float(tick.close))

class MovingAverageCrossoverStrategy(Strategy):
    def __init__(self, risk: float, stop: float):
        self._risk = risk
        self._stop = stop
        self._fast_period = 25
        self._slow_period = 5

    def generate_signals(self, market_data, current_qty, avg_price, symbol) -> list:
        tick = market_data.iloc[-1, :]
        market_data = market_data.to_numpy()
        if len(market_data) < self._fast_period:
            return ('pass', symbol, 0, float(tick.close))
        long = np.mean(market_data[-self._fast_period:])
        short = np.mean(market_data[-self._slow_period:])
        if short > long or tick.close < (1 - self._stop) * avg_price:
            return ('sell', symbol, int(current_qty), float(tick.close))
        elif short < long:
            return ('buy', symbol, int(self._risk // tick.close), float(tick.close))
        else:
            return ('pass', symbol, 0, float(tick.close))


