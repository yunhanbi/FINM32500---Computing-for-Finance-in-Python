# models.py

from dataclasses import dataclass
import datetime
from abc import ABC, abstractmethod
from typing import Optional


# Custom Exceptions
class OrderError(Exception):
    """Exception raised for invalid order parameters."""
    pass


class ExecutionError(Exception):
    """Exception raised during order execution failures."""
    pass


# Immutable data class for market data
@dataclass(frozen=True)
class MarketDataPoint:
    """
    Immutable representation of a single market data tick.
    
    Attributes:
        timestamp: The datetime when this market data was recorded
        symbol: The trading symbol (e.g., 'AAPL')
        price: The price at this timestamp
    """
    timestamp: datetime.datetime
    symbol: str
    price: float

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be positive")


# Mutable class for order management
class Order:
    """
    Mutable class representing a trading order.
    
    Attributes:
        symbol: The trading symbol
        quantity: Number of shares (positive for buy, negative for sell)
        price: The order price
        status: Current order status ('pending', 'filled', 'rejected', 'cancelled')
        timestamp: When the order was created
    """
    
    VALID_STATUSES = ['pending', 'filled', 'rejected', 'cancelled']
    
    def __init__(self, symbol: str, quantity: int, price: float, 
                 status: str = 'pending', timestamp: Optional[datetime.datetime] = None):
        # Validate inputs
        if quantity == 0:
            raise OrderError("Order quantity cannot be zero")
        if price <= 0:
            raise OrderError("Order price must be positive")
        if status not in self.VALID_STATUSES:
            raise OrderError(f"Invalid order status: {status}")
            
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.status = status
        self.timestamp = timestamp or datetime.datetime.now()
    
    def update_status(self, new_status: str) -> None:
        """Update the order status."""
        if new_status not in self.VALID_STATUSES:
            raise OrderError(f"Invalid order status: {new_status}")
        self.status = new_status
    
    def __repr__(self) -> str:
        return (f"Order(symbol='{self.symbol}', quantity={self.quantity}, "
                f"price={self.price:.2f}, status='{self.status}')")


# Portfolio position representation
@dataclass
class Position:
    """Represents a position in a particular symbol."""
    symbol: str
    quantity: int = 0
    avg_price: float = 0.0
    unrealized_pnl: float = 0.0
    
    def update_position(self, trade_qty: int, trade_price: float) -> None:
        """Update position with a new trade."""
        if self.quantity == 0:
            # Opening new position
            self.quantity = trade_qty
            self.avg_price = trade_price
        else:
            # Adding to existing position
            if (self.quantity > 0 and trade_qty > 0) or (self.quantity < 0 and trade_qty < 0):
                # Same direction trade - update average price
                total_cost = (self.quantity * self.avg_price) + (trade_qty * trade_price)
                self.quantity += trade_qty
                if self.quantity != 0:
                    self.avg_price = total_cost / self.quantity
            else:
                # Opposite direction trade - reduce position
                self.quantity += trade_qty
                if self.quantity == 0:
                    self.avg_price = 0.0
    
    def calculate_unrealized_pnl(self, current_price: float) -> float:
        """Calculate unrealized P&L based on current market price."""
        if self.quantity == 0:
            return 0.0
        self.unrealized_pnl = self.quantity * (current_price - self.avg_price)
        return self.unrealized_pnl