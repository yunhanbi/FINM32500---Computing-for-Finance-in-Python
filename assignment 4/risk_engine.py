# risk_engine.py

from order import Order, OrderState
from datetime import datetime


class RiskEngine:
    """Simple Risk Engine to check orders against position and size limits."""
    
    def __init__(self, max_order_size=1000, max_position=2000):
        """
        Initialize risk engine with limits.
        
        Args:
            max_order_size: Maximum allowed order size
            max_position: Maximum allowed position per symbol
        """
        self.max_order_size = max_order_size
        self.max_position = max_position
        # Track positions for multiple symbols
        self.positions = {}  # {symbol: position_quantity}
        print(f"Risk Engine initialized: Max Order={max_order_size}, Max Position={max_position}")
    
    def check(self, order) -> bool:
        """
        Check if order passes all risk checks.
        
        Args:
            order: Order object to check
            
        Returns:
            True if order passes all checks, False if rejected
        """
        # Get current position for this symbol (0 if new symbol)
        current_position = self.positions.get(order.symbol, 0)
        
        # Check 1: Order size limit
        if order.qty > self.max_order_size:
            self._log_rejection(order, f"Order size {order.qty} exceeds max {self.max_order_size}")
            return False
        
        # Check 2: Position limit after this order
        if order.side.upper() == "BUY":
            new_position = current_position + order.qty
        else:  # SELL
            new_position = current_position - order.qty
        
        if abs(new_position) > self.max_position:
            self._log_rejection(order, 
                f"Position would be {new_position}, exceeds max {self.max_position} "
                f"(current: {current_position})")
            return False
        
        # All checks passed
        self._log_approval(order, current_position, new_position)
        return True
    
    def update_position(self, order):
        """
        Update position after order is filled.
        
        Args:
            order: Filled order to update position for
        """
        if order.state != OrderState.FILLED:
            print(f"❌ Cannot update position: Order {order.symbol} not filled (state: {order.state.name})")
            return
        
        # Get current position (0 if new symbol)
        current_position = self.positions.get(order.symbol, 0)
        
        # Update position based on side
        if order.side.upper() == "BUY":
            new_position = current_position + order.qty
        else:  # SELL
            new_position = current_position - order.qty
        
        # Update the position
        self.positions[order.symbol] = new_position
        
        time = datetime.now().strftime("%H:%M:%S")
        print(f"📊 [{time}] Position updated: {order.symbol} {current_position} -> {new_position}")
    
    def get_position(self, symbol):
        """Get current position for a symbol."""
        return self.positions.get(symbol, 0)
    
    def get_all_positions(self):
        """Get all current positions."""
        return dict(self.positions)
    
    def _log_rejection(self, order, reason):
        """Log when order is rejected by risk engine."""
        time = datetime.now().strftime("%H:%M:%S")
        print(f"🚫 [{time}] RISK REJECTION: {order.symbol} {order.qty} {order.side} - {reason}")
    
    def _log_approval(self, order, current_pos, new_pos):
        """Log when order passes risk checks."""
        time = datetime.now().strftime("%H:%M:%S")
        print(f"✅ [{time}] RISK APPROVED: {order.symbol} {order.qty} {order.side} "
               f"(pos: {current_pos} -> {new_pos})")


def process_order_with_risk(order, risk_engine):
    """
    Complete order processing with risk checks.
    Demonstrates: Risk Check -> Acknowledge -> Fill -> Update Position
    """
    print(f"\n--- Processing Order: {order} ---")
    
    # Step 1: Risk check BEFORE acknowledging
    if not risk_engine.check(order):
        order.transition(OrderState.REJECTED)  # Reject the order
        return False
    
    # Step 2: If risk check passes, acknowledge order
    order.transition(OrderState.ACKED)
    
    # Step 3: Fill the order (simulate execution)
    order.transition(OrderState.FILLED)
    
    # Step 4: Update position AFTER fill
    risk_engine.update_position(order)
    
    return True


if __name__ == "__main__":
    print("=== Risk Engine Test ===\n")
    
    # Create risk engine with limits
    risk = RiskEngine(max_order_size=500, max_position=1000)
    
    print("\n--- Test 1: Normal Orders (Should Pass) ---")
    order1 = Order("AAPL", 100, "BUY")
    process_order_with_risk(order1, risk)
    
    order2 = Order("AAPL", 200, "BUY")
    process_order_with_risk(order2, risk)
    
    order3 = Order("MSFT", 150, "SELL")
    process_order_with_risk(order3, risk)
    
    print("\n--- Test 2: Order Size Limit (Should Fail) ---")
    big_order = Order("GOOGL", 600, "BUY")  # Exceeds 500 limit
    process_order_with_risk(big_order, risk)
    
    print("\n--- Test 3: Position Limit (Should Fail) ---")
    # Current AAPL position is +300, adding +800 would = +1100 (exceeds 1000 limit)
    large_buy = Order("AAPL", 800, "BUY")
    process_order_with_risk(large_buy, risk)
    
    print("\n--- Test 4: Multiple Symbols ---")
    order4 = Order("TSLA", 400, "BUY")
    process_order_with_risk(order4, risk)
    
    # Show final positions
    print("\n--- Final Positions ---")
    positions = risk.get_all_positions()
    for symbol, position in positions.items():
        print(f"{symbol}: {position}")
    
    if not positions:
        print("No positions")