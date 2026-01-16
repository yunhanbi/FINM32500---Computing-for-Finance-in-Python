import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
import numpy as np
from models import ExecutionError, Order
from data_loader import data_loader

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick) -> list:
        pass

class MomentumStrategy(Strategy):
    def __init__(self, risk: float, stop: float):
        super().__init__(risk, stop)
        self._history_mm = np.array([])
        self._period = 3
        self._adx_target = 25
        self._rsi_target = (45, 55)
        self._window = 15
        self.__adx = None
        self.__dm_pos = None
        self.__dm_neg = None
        self.__tr = None

    def generate_adx(self, vec):
        vec_res = vec[-(((self._window // self._period)) + 1) * self._period:].reshape(-1, self._period)
        vec_max = np.max(vec_res, axis=-1)[1:]
        vec_min = np.min(vec_res, axis=-1)[1:]
        vec_cls = vec_res[:-1, -1]
        tr = np.max(np.vstack((vec_max - vec_min, vec_max - vec_cls, vec_min - vec_cls)), axis=0)
        dm_pos = np.maximum(np.diff(vec_max), 0)
        dm_neg = np.maximum(-np.diff(vec_min), 0)
        dm_diff = dm_pos > dm_neg
        dm_pos[~dm_diff] = 0
        dm_neg[dm_diff] = 0
        self.__dm_pos = np.mean(dm_pos) if self.__dm_pos is None else self.__dm_pos * (
                    1 - (1 / ((self._window // self._period)))) + np.mean(dm_pos) * (1 / (self._window // self._period))
        self.__dm_neg = np.mean(dm_neg) if self.__dm_neg is None else self.__dm_neg * (
                    1 - (1 / ((self._window // self._period)))) + np.mean(dm_neg) * (1 / (self._window // self._period))
        self.__tr = np.mean(tr) if self.__tr is None else self.__tr * (
                    1 - (1 / ((self._window // self._period)))) + np.mean(tr) * (1 / (self._window // self._period))
        di_pos = (self.__dm_pos / self.__tr) * 100
        di_neg = (self.__dm_neg / self.__tr) * 100
        self.__adx = (abs(di_pos - di_neg) / (di_pos + di_neg)) * 100
        return [self.__adx, 'uptrend' if di_pos > di_neg else 'downtrend']

    def generate_rsi(self, vec):
        diff = np.diff(vec[-self._window:])
        avg_gain = diff[diff > 0].mean()
        avg_loss = abs(diff[diff <= 0].mean())
        return 100 - (100 / (1 + (avg_gain / avg_loss)))

    def generate_signals(self, tick, current_qty, avg_price) -> list:
        self._history_mm = np.append(self._history_mm, tick.price)
        if len(self._history_mm) < self._window + self._period:
            print('Waiting for more history')
            return ('pass', tick.symbol, 0, float(tick.price))
        vec = self._history_mm[-(self._window + self._period):]
        adx = self.generate_adx(vec)
        if adx[0] < self._adx_target:
            # print('Not a strong trend')
            return ('pass', tick.symbol, 0, float(tick.price))
        elif adx[1] == 'uptrend' and self.generate_rsi(vec) < self._rsi_target[0]:
            return ('buy', tick.symbol, int(self._risk // tick.price), float(tick.price))
        elif adx[1] == 'downtrend' and self.generate_rsi(vec) > self._rsi_target[1]:
            return ('sell', tick.symbol, int(current_qty), float(tick.price))
        else:
            return ('pass', tick.symbol, 0, float(tick.price))

class MovingAverageCrossoverStrategy(Strategy):
    def __init__(self, risk: float, stop: float):
        self._risk = risk
        self._stop = stop
        self._fast_period = 25
        self._slow_period = 5
        self._history_mac = np.array([])

    def generate_signals(self, tick, current_qty, avg_price) -> list:
        self._history_mac = np.append(self._history_mac, tick.price)
        if len(self._history_mac) < self._fast_period:
            print('Waiting for more history')
            return ('pass', tick.symbol, 0, float(tick.price))
        long = np.mean(self._history_mac[-self._fast_period:])
        short = np.mean(self._history_mac[-self._slow_period:])
        if short > long or tick.price < (1 - self._stop) * avg_price:
            return ('sell', tick.symbol, int(current_qty), float(tick.price))
        elif short < long:
            return ('buy', tick.symbol, int(self._risk // tick.price), float(tick.price))
        else:
            return ('pass', tick.symbol, 0, float(tick.price))