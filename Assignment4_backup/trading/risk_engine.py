class RiskEngine:
    def __init__(self, max_order_size=1000, max_position=2000):
        self.position = 0
        self.max_order_size = max_order_size
        self.max_position = max_position
        pass

    def check(self, order) -> bool:
        position = (1 if order.side == "1" else -1) * order.qty + self.position
        if order.qty > self.max_order_size or position < 0 or position > self.max_position:
            raise ValueError(rf'{'buy' if order.side == '1' else 'sell'} {order.qty} can not be executed for {order.symbol} with position {self.position}.')
        pass

    def update_position(self, order):
        self.position += (1 if order.side == "1" else -1) * order.qty
        pass