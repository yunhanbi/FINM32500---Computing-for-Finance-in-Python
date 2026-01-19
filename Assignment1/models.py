from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float

class OrderError(Exception):
    pass

class ExecutionError(Exception):
    pass

class Order:
    def __init__(self, action, symbol, quantity, price):
        if quantity <= 0:
            raise OrderError(f"Quantity must be positive: {quantity}")
        if price <= 0:
            raise OrderError(f"Price must be positive: {price}")
        
        self.action = action  # 'BUY' or 'SELL'
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.status = 'PENDING'
    
    def execute(self):
        self.status = 'EXECUTED'
