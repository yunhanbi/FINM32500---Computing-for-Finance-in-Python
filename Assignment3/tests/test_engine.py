import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

from unittest.mock import MagicMock
from ..trading.engine import Engine
from ..trading.subject import MarketDataSubject
from ..trading.broker import Broker

def test_engine_uses_strategy_signal(prices):
    subject = MarketDataSubject()
    fake_strategy = MagicMock()
    fake_strategy.last_signal = 1

    broker = Broker(cash=1_000)

    # Attach fake strategy as an observer
    subject.attach(fake_strategy)

    engine = Engine(subject, fake_strategy, broker)

    # You can control fake_strategy.last_signal over time via side_effect
    # or by updating it in a custom observer implementation for more realism.

    equity = engine.run(prices)
    return equity
    # Assert broker was called appropriately, equity consistent, etc.

print(test_engine_uses_strategy_signal([1,1,1]))