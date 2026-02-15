import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

from trading.broker import Broker
from unittest.mock import MagicMock
import pytest

def test_invalid_market_order():
    obj = Broker()
    with pytest.raises(ValueError):
        obj.market_order('buy', 11, 111000)

def test_valid_market_order():
    obj = Broker()
    obj.market_order('buy', 10, 100)

    assert obj.cash == (1000000 + 1000)
