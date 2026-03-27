import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

from trading.subject import MarketDataSubject
from trading.observers import VolatilityBreakoutStrategyObserver
from unittest.mock import MagicMock

def test_logger_records_all_prices(subject, logger, prices):
    subject.attach(logger)
    for p in prices:
        subject.notify(float(p))

    assert logger.prices[0] == float(prices.iloc[0])
    assert len(logger.prices) == len(prices)

def test_strategy_last_signal(subject, strategy, prices):
    subject.attach(strategy)
    signals = []
    for p in prices:
        subject.notify(float(p))
        signals.append(strategy.last_signal)

    assert strategy.last_signal == signals[-1]
    assert len(signals) == len(prices)

