# logger.py

from datetime import datetime
import json
import os


class Logger:
    """
    Singleton Logger class to record all system events.
    Records order creation, state changes, and risk events.
    """
    
    _instance = None  # Singleton instance
    
    def __new__(cls, path="events.json"):
        """Ensure only one logger instance exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, path="events.json"):
        """Initialize logger only once."""
        if self._initialized:
            return  # Already initialized
        
        self.path = path
        self.events = []
        self._initialized = True
        print(f"📝 Logger initialized: {path}")
    
    def log(self, event_type, data):
        """
        Log an event with timestamp.
        
        Args:
            event_type: Type of event (e.g., 'ORDER_CREATED', 'STATE_CHANGE', 'RISK_CHECK')
            data: Event data (dictionary with relevant information)
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        
        self.events.append(event)
        
        # Print to console for immediate feedback
        time_str = datetime.now().strftime("%H:%M:%S")
        print(f"📝 [{time_str}] {event_type}: {data}")
    
    def save(self):
        """Save all events to JSON file."""
        try:
            with open(self.path, 'w') as f:
                json.dump(self.events, f, indent=2)
            print(f"💾 Saved {len(self.events)} events to {self.path}")
        except Exception as e:
            print(f"❌ Error saving events: {e}")
    
    def load_events(self):
        """Load existing events from file (optional helper method)."""
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.events = json.load(f)
                print(f"📁 Loaded {len(self.events)} existing events")
            except Exception as e:
                print(f"❌ Error loading events: {e}")
                self.events = []
    
    def get_events_by_type(self, event_type):
        """Get all events of a specific type."""
        return [event for event in self.events if event['event_type'] == event_type]
    
    def clear_events(self):
        """Clear all events (for testing)."""
        self.events = []
        print("🧹 Cleared all events")
    
    def __len__(self):
        """Return number of logged events."""
        return len(self.events)


# Helper functions to make logging easier
def log_order_created(symbol, qty, side, order_id):
    """Log when order is created."""
    logger = Logger()
    logger.log('ORDER_CREATED', {
        'symbol': symbol,
        'quantity': qty,
        'side': side,
        'order_id': order_id
    })


def log_state_change(order_id, from_state, to_state, success):
    """Log when order state changes."""
    logger = Logger()
    logger.log('STATE_CHANGE', {
        'order_id': order_id,
        'from_state': from_state,
        'to_state': to_state,
        'success': success
    })


def log_risk_check(order_id, symbol, qty, side, passed, reason=None):
    """Log risk check results."""
    logger = Logger()
    logger.log('RISK_CHECK', {
        'order_id': order_id,
        'symbol': symbol,
        'quantity': qty,
        'side': side,
        'passed': passed,
        'reason': reason
    })


def log_position_update(symbol, old_position, new_position):
    """Log position updates."""
    logger = Logger()
    logger.log('POSITION_UPDATE', {
        'symbol': symbol,
        'old_position': old_position,
        'new_position': new_position,
        'change': new_position - old_position
    })


if __name__ == "__main__":
    print("=== Event Logger Test ===\n")
    
    # Test singleton behavior
    logger1 = Logger("test_events.json")
    logger2 = Logger("different_path.json")  # Should use same instance
    
    print(f"Same instance? {logger1 is logger2}")  # Should be True
    print()
    
    # Test logging different event types
    print("--- Logging Test Events ---")
    
    # Order creation
    log_order_created("AAPL", 100, "BUY", "ORD001")
    log_order_created("MSFT", 50, "SELL", "ORD002")
    
    # State changes
    log_state_change("ORD001", "NEW", "ACKED", True)
    log_state_change("ORD001", "ACKED", "FILLED", True)
    log_state_change("ORD002", "NEW", "FILLED", False)  # Invalid transition
    
    # Risk checks
    log_risk_check("ORD001", "AAPL", 100, "BUY", True)
    log_risk_check("ORD003", "GOOGL", 2000, "BUY", False, "Exceeds order size limit")
    
    # Position updates
    log_position_update("AAPL", 0, 100)
    log_position_update("MSFT", 200, 150)
    
    print(f"\nTotal events logged: {len(logger1)}")
    
    # Save events to file
    logger1.save()
    
    # Show events by type
    print("\n--- Events by Type ---")
    order_events = logger1.get_events_by_type('ORDER_CREATED')
    print(f"Order Created Events: {len(order_events)}")
    
    risk_events = logger1.get_events_by_type('RISK_CHECK')
    print(f"Risk Check Events: {len(risk_events)}")
    
    # Show sample event structure
    if logger1.events:
        print("\n--- Sample Event Structure ---")
        print(json.dumps(logger1.events[0], indent=2))