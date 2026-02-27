import pytest
import json
import os
from fix_parser import FixParser
from order import Order, OrderState
from risk_engine import RiskEngine
from logger import Logger


class TestFixParser:
    """Test FIX message parsing functionality."""
    
    def setup_method(self):
        """Setup for each test."""
        self.parser = FixParser()
    
    def test_valid_order_parsing(self):
        """Test parsing valid order message."""
        msg = "8=FIX.4.2|35=D|55=AAPL|54=1|38=100|40=2|10=128"
        result = self.parser.parse(msg)
        
        assert result['BeginString'] == 'FIX.4.2'
        assert result['Symbol'] == 'AAPL'
        assert result['Side'] == '1'
    
    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        msg = "8=FIX.4.2|35=D|54=1|38=100|40=2|10=128"  # Missing Symbol
        
        with pytest.raises(ValueError):
            self.parser.parse(msg)


class TestOrder:
    """Test order lifecycle functionality."""
    
    def setup_method(self):
        """Setup for each test."""
        self.order = Order("AAPL", 100, "BUY")
    
    def test_order_creation(self):
        """Test order is created correctly."""
        assert self.order.symbol == "AAPL"
        assert self.order.qty == 100
        assert self.order.side == "BUY"
        assert self.order.state == OrderState.NEW
    
    def test_valid_transitions(self):
        """Test valid state transitions."""
        # NEW -> ACKED
        result = self.order.transition(OrderState.ACKED)
        assert result is True
        assert self.order.state == OrderState.ACKED


class TestRiskEngine:
    """Test risk engine functionality."""
    
    def setup_method(self):
        """Setup for each test."""
        self.risk_engine = RiskEngine(max_order_size=500, max_position=1000)
    
    def test_order_size_check_pass(self):
        """Test order passes size check."""
        order = Order("AAPL", 100, "BUY")
        result = self.risk_engine.check(order)
        assert result is True
    
    def test_order_size_check_fail(self):
        """Test order fails size check."""
        order = Order("AAPL", 600, "BUY")  # Exceeds max 500
        result = self.risk_engine.check(order)
        assert result is False


class TestLogger:
    """Test logging functionality."""
    
    def setup_method(self):
        """Setup for each test."""
        self.test_file = "test_events.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.logger = Logger(self.test_file)
        self.logger.clear_events()
    
    def test_logging_events(self):
        """Test event logging."""
        self.logger.log("TEST_EVENT", {"key": "value"})
        
        assert len(self.logger) == 1
        event = self.logger.events[0]
        assert event['event_type'] == "TEST_EVENT"


if __name__ == "__main__":
    pytest.main(["-v", __file__])