# fix_parser.py
class FixParser:
    """Simplified FIX Parser focusing on essential trading fields."""
    
    # Essential FIX tags for trading
    ESSENTIAL_TAGS = {
        8: 'BeginString',
        9: 'BodyLength', 
        35: 'MsgType',
        49: 'SenderCompID',
        56: 'TargetCompID',
        34: 'MsgSeqNum',
        52: 'SendingTime',
        55: 'Symbol',
        54: 'Side',
        40: 'OrdType',
        11: 'ClOrdID',
        39: 'OrdStatus',
        150: 'ExecType',
        60: 'TransactTime',
        10: 'CheckSum'
    }
    
    # Core message types
    MSG_TYPES = {
        'D': 'NewOrderSingle',
        '8': 'ExecutionReport',
        'F': 'OrderCancelRequest'
    }
    
    # Side values (most important)
    SIDES = {
        '1': 'Buy',
        '2': 'Sell'
    }
    
    # Order types (essential)
    ORDER_TYPES = {
        '1': 'Market',
        '2': 'Limit'
    }
    
    def parse(self, fix_message: str) -> dict:
        """Parse FIX message using essential tags only."""
        fields = fix_message.split('|')
        parsed = {}
        
        for field in fields:
            if '=' not in field:
                continue
                
            tag, value = field.split('=', 1)
            tag_num = int(tag)
            
            # Only parse essential tags
            if tag_num in self.ESSENTIAL_TAGS:
                field_name = self.ESSENTIAL_TAGS[tag_num]
                parsed[field_name] = value
        
        # Validate required fields
        self._validate_essential_fields(parsed)
        
        return parsed
    
    def _validate_essential_fields(self, parsed: dict) -> None:
        """Validate only the most critical fields."""
        # Always required
        if 'MsgType' not in parsed:
            raise ValueError("Missing MsgType (tag 35)")
        
        # For trading messages, require these fields
        if parsed.get('MsgType') == 'D':  # New Order
            required = ['Symbol', 'Side', 'OrdType']
            for field in required:
                if field not in parsed:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate side
            side = parsed.get('Side')
            if side not in self.SIDES:
                raise ValueError(f"Invalid side: {side}")


if __name__ == "__main__":
    parser = FixParser()
    
    # Test with essential fields only
    msg = "8=FIX.4.2|35=D|55=AAPL|54=1|40=2|11=ORDER123|10=128"
    result = parser.parse(msg)
    print("Simplified parser result:")
    for key, value in result.items():
        print(f"  {key}: {value}")