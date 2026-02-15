import numpy as np
import pandas as pd
from typing import Optional

class VolatilityBreakoutStrategyObserver:
    def __init__(self, window: int = 20):
        self.window = window
        self._prices: list[float] = []
        self._last_signal: int = 0

    def update(self, price: float) -> None:
        self._prices.append(price)
        if len(self._prices) < window:
            pass
        rolling_std = np.std(self._prices[-window:])
        rolling_mean = np.mean(self._prices[-window:])
        if price > rolling_mean + 2 * rolling_std:
            self._last_signal = 1
        elif price < rolling_mean - 2 * rolling_std:
            self._last_signal = -1
        else:
            self._last_signal = 0
        pass

    @property
    def last_signal(self) -> int:
        return self._last_signal


class RiskObserver:
    def __init__(self, max_position: int):
        self.max_position = max_position
        self.breached = False

    def update(self, price: float) -> None:
        return self.max_position * price


class LoggerObserver:
    def __init__(self):
        self.prices: list[float] = []

    def update(self, price: float) -> None:
        self.prices.append(price)
        pass