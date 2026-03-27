class Broker:
    def __init__(self, cash: float = 1_000_000):
        self.cash = cash
        self.position = 0

    def market_order(self, side: str, qty: int, price: float) -> None:
        if (self.cash < price * qty) or (self.position + qty < 0):
            raise ValueError()
        self.cash += price * qty
        self.position += qty
        pass