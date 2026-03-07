import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

from trading.risk_engine import RiskEngine
from unittest.mock import MagicMock
import pytest

def test_risk_engine():
    engine = RiskEngine()
    test_order = MagicMock()
    test_order.symbol = "AAPL"
    test_order.side = 1
    test_order.qty = 5000
    with pytest.raises(ValueError):
        engine.check(test_order)

def test_update_position():
    engine = RiskEngine()
    test_order = MagicMock()
    test_order.qty  = 100
    test_order.side = 1
    engine.update_position(test_order)
    assert test_order.qty == 100