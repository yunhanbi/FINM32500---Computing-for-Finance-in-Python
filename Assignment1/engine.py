from models import Order, OrderError, ExecutionError

class Portfolio:
    def __init__(self, cash=100000):
        self.cash = cash
        self.positions = {}
        self.history = []
    
    def execute_order(self, order):
        if order.action == 'BUY':
            cost = order.quantity * order.price
            if cost > self.cash:
                raise ExecutionError("Insufficient cash")
            self.cash -= cost
            self.positions[order.symbol] = self.positions.get(order.symbol, 0) + order.quantity
        
        elif order.action == 'SELL':
            if self.positions.get(order.symbol, 0) < order.quantity:
                raise ExecutionError("Insufficient shares")
            self.cash += order.quantity * order.price
            self.positions[order.symbol] -= order.quantity
        
        order.execute()
        self.history.append((order.action, order.symbol, order.quantity, order.price))
    
    def value(self, prices):
        total = self.cash
        for symbol, qty in self.positions.items():
            total += qty * prices.get(symbol, 0)
        return total

class BacktestEngine:
    def __init__(self, strategies):
        self.strategies = strategies
        self.portfolio = Portfolio()
        self.errors = []
    
    def run(self, market_data):
        prices = {}
        
        for tick in market_data:
            prices[tick.symbol] = tick.price
            
            for strategy in self.strategies:
                signals = strategy.generate_signals(tick)
                
                for signal in signals:
                    try:
                        action, symbol, qty, price = signal
                        order = Order(action, symbol, qty, price)
                        self.portfolio.execute_order(order)
                    except (OrderError, ExecutionError) as e:
                        self.errors.append(str(e))
        
        return self.portfolio
