# main.py for integration

from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger
import json


class TradingSystem:
    """Complete trading system integrating all components."""
    
    def __init__(self):
        """Initialize all system components."""
        self.fix_parser = FixParser()
        self.risk_engine = RiskEngine(max_order_size=1000, max_position=2000)
        self.logger = Logger("trading_events.json")
        self.orders = {}  # Track all orders by ID
        self.order_counter = 1
        
        print("🚀 Trading System Initialized")
        print("-" * 50)
    
    def process_fix_message(self, raw_message):
        """
        Process a single FIX message through the complete workflow.
        
        Args:
            raw_message: Raw FIX protocol string
        """
        try:
            print(f"\n📨 Processing: {raw_message}")
            
            # Step 1: Parse FIX message
            parsed_msg = self.fix_parser.parse(raw_message)
            print(f"✅ Parsed successfully: {parsed_msg.get('Symbol', 'Unknown')} "
                  f"{parsed_msg.get('Side_Decoded', 'Unknown')}")
            
            # Step 2: Create Order object
            order = self._create_order_from_fix(parsed_msg)
            if not order:
                return
            
            # Step 3: Log order creation
            self.logger.log("ORDER_CREATED", {
                'order_id': order.order_id,
                'symbol': order.symbol,
                'quantity': order.qty,
                'side': order.side,
                'raw_fix': raw_message
            })
            
            # Step 4: Risk check
            if not self.risk_engine.check(order):
                # Risk check failed - reject order
                order.transition(OrderState.REJECTED)
                self.logger.log("ORDER_REJECTED", {
                    'order_id': order.order_id,
                    'symbol': order.symbol,
                    'reason': 'Risk check failed'
                })
                return
            
            # Step 5: Acknowledge order
            order.transition(OrderState.ACKED)
            self.logger.log("ORDER_ACKNOWLEDGED", {
                'order_id': order.order_id,
                'symbol': order.symbol
            })
            
            # Step 6: Fill order (simulate execution)
            order.transition(OrderState.FILLED)
            self.risk_engine.update_position(order)
            
            self.logger.log("ORDER_FILLED", {
                'order_id': order.order_id,
                'symbol': order.symbol,
                'quantity': order.qty,
                'side': order.side
            })
            
            print(f"✅ Order {order.order_id} completed successfully")
            
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            if 'order' in locals():
                order.transition(OrderState.REJECTED)
                self.logger.log("ORDER_ERROR", {
                    'order_id': order.order_id if 'order' in locals() else 'Unknown',
                    'error': str(e),
                    'raw_message': raw_message
                })
    
    def _create_order_from_fix(self, parsed_msg):
        """Create Order object from parsed FIX message."""
        try:
            # Extract required fields from FIX message
            symbol = parsed_msg.get('Symbol')
            qty_str = parsed_msg.get('OrderQty', parsed_msg.get('38'))  # Try tag name then number
            side = parsed_msg.get('Side_Decoded', parsed_msg.get('Side'))
            
            if not symbol:
                raise ValueError("Missing symbol in FIX message")
            if not qty_str:
                raise ValueError("Missing quantity in FIX message")
            if not side:
                raise ValueError("Missing side in FIX message")
            
            # Convert quantity to integer
            qty = int(qty_str)
            
            # Generate order ID
            order_id = f"ORD_{self.order_counter:04d}"
            self.order_counter += 1
            
            # Create order
            order = Order(symbol, qty, side)
            order.order_id = order_id  # Add order ID
            
            # Store order
            self.orders[order_id] = order
            
            return order
            
        except Exception as e:
            print(f"❌ Error creating order: {e}")
            return None
    
    def process_multiple_messages(self, messages):
        """Process a list of FIX messages."""
        print(f"\n🔄 Processing {len(messages)} messages...")
        
        for i, message in enumerate(messages, 1):
            print(f"\n{'='*20} Message {i}/{len(messages)} {'='*20}")
            self.process_fix_message(message)
        
        # Save all events at the end
        self.logger.save()
        
        # Show summary
        self._show_summary()
    
    def _show_summary(self):
        """Show system summary after processing."""
        print("\n" + "="*60)
        print("📊 TRADING SYSTEM SUMMARY")
        print("="*60)
        
        # Order summary
        total_orders = len(self.orders)
        filled_orders = len([o for o in self.orders.values() if o.state == OrderState.FILLED])
        rejected_orders = len([o for o in self.orders.values() if o.state == OrderState.REJECTED])
        
        print(f"Total Orders: {total_orders}")
        print(f"Filled Orders: {filled_orders}")
        print(f"Rejected Orders: {rejected_orders}")
        
        # Position summary
        positions = self.risk_engine.get_all_positions()
        print(f"\nCurrent Positions:")
        if positions:
            for symbol, position in positions.items():
                print(f"  {symbol}: {position:+}")
        else:
            print("  No positions")
        
        # Event summary
        print(f"\nTotal Events Logged: {len(self.logger)}")
        print(f"Events saved to: {self.logger.path}")


def get_sample_fix_messages():
    """Generate sample FIX messages for testing."""
    return [
        # Valid orders
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128",
        "8=FIX.4.2|35=D|55=MSFT|54=2|38=200|40=1|10=129",  
        "8=FIX.4.2|35=D|55=GOOGL|54=1|38=50|40=2|10=130",
        
        # Orders that should trigger risk checks
        "8=FIX.4.2|35=D|55=AAPL|54=1|38=1500|40=2|10=131",  # Too large
        "8=FIX.4.2|35=D|55=TSLA|54=1|38=500|40=2|10=132",   # OK
        
        # More normal orders
        "8=FIX.4.2|35=D|55=AAPL|54=2|38=300|40=1|10=133",   # Reduce AAPL position
        "8=FIX.4.2|35=D|55=MSFT|54=1|38=100|40=2|10=134",   # Reverse MSFT
    ]


if __name__ == "__main__":
    print("🏦 INTEGRATED TRADING SYSTEM")
    print("="*60)
    
    # Initialize trading system
    system = TradingSystem()
    
    # Get sample messages
    messages = get_sample_fix_messages()
    
    # Process all messages
    system.process_multiple_messages(messages)
    
    print("\n🎯 Integration Complete!")
    print("Check 'trading_events.json' for complete event log.")