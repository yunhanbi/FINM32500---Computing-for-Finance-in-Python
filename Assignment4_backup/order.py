from enum import Enum, auto
from .logger import Logger

log = Logger()

class OrderState(Enum):
    NEW = auto()
    ACKED = auto()
    FILLED = auto()
    CANCELED = auto()
    REJECTED = auto()

class Order:
    def __init__(self, symbol, qty, side):
        self.state = OrderState.NEW
        self.symbol = symbol
        self.qty = qty
        self.side = side

    def transition(self, new_state):
        allowed = {
            OrderState.NEW: {OrderState.ACKED, OrderState.REJECTED},
            OrderState.ACKED: {OrderState.FILLED, OrderState.CANCELED},
        }
        if new_state in allowed[self.state]:
            self.state = new_state
            print(rf'Order {self.symbol} is {self.state}')
        else:
            raise ValueError(rf'Order {self.symbol} is not allowed to transition from {self.state} to {new_state}')
