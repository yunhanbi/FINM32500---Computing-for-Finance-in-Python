import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
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
    def __init__(self, status, symbol, quantity, price):
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.status = status

    def update_portfolio(self, position):
        try:
            if self.quantity < 0:
                raise OrderError('Quantity cannot be negative')
            if self.symbol not in position.keys():
                raise OrderError('Action symbol not in portfolio')

            if self.status == 'buy':
                position[self.symbol]['avg_price'] = (position[self.symbol]['quantity']*position[self.symbol]['avg_price'] + self.quantity * self.price)/(position[self.symbol]['quantity'] + self.quantity)
                position[self.symbol]['quantity'] += self.quantity
                return [position, -self.quantity * self.price]
            elif self.status == 'sell':
                if self.quantity > position[self.symbol]['quantity']:
                    raise OrderError('Sell more than portfolio quantity')
                position[self.symbol]['quantity'] -= self.quantity
                if position[self.symbol]['quantity'] == 0:
                    position[self.symbol]['avg_price'] = 0
                return [position, self.price * self.quantity]
            elif self.status == 'pass':
                return [position, 0]
            else:
                raise OrderError('Action is not recognized')

        except OrderError as err:
            return err

        except Exception as err:
            return err