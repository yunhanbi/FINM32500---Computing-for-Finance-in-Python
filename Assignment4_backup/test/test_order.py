import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

from ..order import Order, OrderState
from ..fix_parser import FixParser
import pytest

fix = FixParser()
raw = "8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128"
msg = fix.parse(raw)

def test_order():
    order = Order(msg["55"], int(msg["38"]), msg["54"])
    assert order.state == OrderState.NEW

def test_order_transition():
    order = Order(msg["55"], int(msg["38"]), msg["54"])
    order.transition(OrderState.ACKED)
    assert order.state == OrderState.ACKED

def test_order_transition_exception():
    order = Order(msg["55"], int(msg["38"]), msg["54"])
    with pytest.raises(ValueError):
            order.transition(OrderState.CANCELED)
