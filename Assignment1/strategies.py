from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick):
        pass

class MovingAverageStrategy(Strategy):
    def __init__(self):
        self.prices = []
        self.position = 0
    
    def generate_signals(self, tick):
        self.prices.append(tick.price)
        
        if len(self.prices) < 20:
            return []
        
        short_ma = sum(self.prices[-5:]) / 5
        long_ma = sum(self.prices[-20:]) / 20
        
        signals = []
        if short_ma > long_ma and self.position == 0:
            signals.append(('BUY', tick.symbol, 100, tick.price))
            self.position = 100
        elif short_ma < long_ma and self.position > 0:
            signals.append(('SELL', tick.symbol, self.position, tick.price))
            self.position = 0
        
        return signals
