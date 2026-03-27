import pandas as pd
from .subject import MarketDataSubject
from .observers import VolatilityBreakoutStrategyObserver
from .broker import Broker

class Engine:
    def __init__(
        self,
        subject: MarketDataSubject,
        strategy: VolatilityBreakoutStrategyObserver,
        broker: Broker,
    ):
        self.subject = subject
        self.strategy = strategy
        self.broker = broker

    def run(self, prices: pd.Series) -> float:
        for price in prices:
            self.subject.notify(price)
            signal = self.strategy.last_signal
            if signal != 0:
                self.broker.market_order('buy' if signal > 0 else 'sell', signal, price)
        return self.broker.cash + self.broker.position * price
