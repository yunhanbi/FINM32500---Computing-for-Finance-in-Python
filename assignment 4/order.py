# order.py
# Enum (Enumeration) is a Python class that creates a set of named constants. It's good for representing fixed sets of values like order states
# Enum makes the trading system safer and more maintainable 

from enum import Enum, auto
from datetime import datetime


class OrderState(Enum):
    NEW = auto()
    ACKED = auto()
    FILLED = auto()
    CANCELED = auto()
    REJECTED = auto()


class Order:
    """Simple Order class to track order lifecycle."""
    
    def __init__(self, symbol, qty, side):
        """Create a new order."""
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.state = OrderState.NEW
        print(f"Created order: {symbol} {qty} {side} - State: {self.state.name}")
    
    def transition(self, new_state):
        """
        Try to change order state. Log if transition is not allowed.
        
        Args:
            new_state: The state we want to change to
            
        Returns:
            True if successful, False if not allowed
        """
        # Define what transitions are allowed from each state
        allowed = {
            OrderState.NEW: {OrderState.ACKED, OrderState.REJECTED},
            OrderState.ACKED: {OrderState.FILLED, OrderState.CANCELED},
            # FILLED, CANCELED, REJECTED can't transition anywhere (terminal states)
        }
        
        current_state = self.state
        
        # Check if this transition is allowed
        if current_state not in allowed:
            # Current state has no allowed transitions (terminal state)
            self._log_invalid_transition(current_state, new_state)
            return False
        
        if new_state not in allowed[current_state]:
            # Transition not in allowed list
            self._log_invalid_transition(current_state, new_state)
            return False
        
        # Transition is allowed - do it!
        self.state = new_state
        self._log_successful_transition(current_state, new_state)
        return True
    
    def _log_successful_transition(self, from_state, to_state):
        """Log when transition succeeds."""
        time = datetime.now().strftime("%H:%M:%S")
        print(f"✅ [{time}] {self.symbol}: {from_state.name} -> {to_state.name}")
    
    def _log_invalid_transition(self, from_state, to_state):
        """Log when transition is not allowed."""
        time = datetime.now().strftime("%H:%M:%S")
        print(f"❌ [{time}] {self.symbol}: INVALID {from_state.name} -> {to_state.name}")
    
    def __str__(self):
        """Show order details when printed."""
        return f"{self.symbol} {self.qty} {self.side} [{self.state.name}]"


if __name__ == "__main__":
    # Test the simple order lifecycle
    print("=== Simple Order Lifecycle Test ===\n")
    
    # Create order
    order = Order("AAPL", 100, "BUY")
    print(f"Order: {order}\n")
    
    # Valid transitions
    print("--- Valid Transitions ---")
    order.transition(OrderState.ACKED)    # NEW -> ACKED (allowed)
    order.transition(OrderState.FILLED)   # ACKED -> FILLED (allowed)
    print()
    
    # Invalid transitions
    print("--- Invalid Transitions ---")
    order.transition(OrderState.CANCELED) # FILLED -> CANCELED (not allowed!)
    print()
    
    # Test another order
    print("--- Another Order Test ---")
    order2 = Order("MSFT", 50, "SELL")
    order2.transition(OrderState.FILLED)   # NEW -> FILLED (not allowed!)
    order2.transition(OrderState.ACKED)    # NEW -> ACKED (allowed)
    order2.transition(OrderState.CANCELED) # ACKED -> CANCELED (allowed)
    
    print(f"\nFinal states:")
    print(f"Order 1: {order}")
    print(f"Order 2: {order2}")