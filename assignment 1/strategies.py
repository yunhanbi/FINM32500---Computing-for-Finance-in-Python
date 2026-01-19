# strategies.py

from abc import ABC, abstractmethod
from typing import List, Tuple
from collections import deque
from models import MarketDataPoint


class Strategy(ABC):
    """
    Abstract base class for trading strategies.
    
    All strategies must implement the generate_signals method to produce
    trading signals based on market data.
    """
    
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> List[Tuple[str, str, int, float]]:
        """
        Generate trading signals based on the current market tick.
        
        Args:
            tick: Current market data point
            
        Returns:
            List of tuples in format (action, symbol, quantity, price)
            where action is 'buy' or 'sell'
        """
        pass


class MovingAverageCrossoverStrategy(Strategy):
    """
    Moving Average Crossover Strategy.
    
    Generates buy signals when short MA crosses above long MA,
    and sell signals when short MA crosses below long MA.
    """
    
    def __init__(self, short_window: int = 10, long_window: int = 20, position_size: int = 100):
        """
        Initialize the strategy.
        
        Args:
            short_window: Period for short moving average
            long_window: Period for long moving average
            position_size: Number of shares to trade
        """
        self._short_window = short_window
        self._long_window = long_window
        self._position_size = position_size
        
        # Private attributes for price history
        self._prices = deque(maxlen=long_window)
        self._short_ma = None
        self._long_ma = None
        self._prev_short_ma = None
        self._prev_long_ma = None
        self._position = 0  # Current position: 0 = flat, 1 = long, -1 = short
        
    def _calculate_moving_averages(self) -> Tuple[float, float]:
        """Calculate short and long moving averages."""
        if len(self._prices) < self._short_window:
            return None, None
            
        # Short MA
        short_ma = sum(list(self._prices)[-self._short_window:]) / self._short_window
        
        # Long MA
        if len(self._prices) < self._long_window:
            long_ma = None
        else:
            long_ma = sum(self._prices) / len(self._prices)
            
        return short_ma, long_ma
    
    def generate_signals(self, tick: MarketDataPoint) -> List[Tuple[str, str, int, float]]:
        """Generate signals based on moving average crossover."""
        signals = []
        
        # Add new price to history
        self._prices.append(tick.price)
        
        # Store previous MAs
        self._prev_short_ma = self._short_ma
        self._prev_long_ma = self._long_ma
        
        # Calculate current MAs
        self._short_ma, self._long_ma = self._calculate_moving_averages()
        
        # Need at least 2 MA calculations to detect crossover
        if (self._short_ma is None or self._long_ma is None or 
            self._prev_short_ma is None or self._prev_long_ma is None):
            return signals
        
        # Detect crossovers
        prev_above = self._prev_short_ma > self._prev_long_ma
        curr_above = self._short_ma > self._long_ma
        
        # Golden cross: short MA crosses above long MA (buy signal)
        if not prev_above and curr_above and self._position <= 0:
            if self._position == -1:
                # Close short position first
                signals.append(('buy', tick.symbol, self._position_size, tick.price))
            # Open long position
            signals.append(('buy', tick.symbol, self._position_size, tick.price))
            self._position = 1
            
        # Death cross: short MA crosses below long MA (sell signal)
        elif prev_above and not curr_above and self._position >= 0:
            if self._position == 1:
                # Close long position first
                signals.append(('sell', tick.symbol, self._position_size, tick.price))
            # Open short position
            signals.append(('sell', tick.symbol, self._position_size, tick.price))
            self._position = -1
            
        return signals


class MomentumStrategy(Strategy):
    """
    Momentum Strategy.
    
    Buys when price momentum is positive and sells when negative.
    Uses rate of change over a specified lookback period.
    """
    
    def __init__(self, lookback_period: int = 5, momentum_threshold: float = 0.02, 
                 position_size: int = 100):
        """
        Initialize the momentum strategy.
        
        Args:
            lookback_period: Number of periods to calculate momentum
            momentum_threshold: Minimum momentum to trigger signal
            position_size: Number of shares to trade
        """
        self._lookback_period = lookback_period
        self._momentum_threshold = momentum_threshold
        self._position_size = position_size
        
        # Private attributes for price history
        self._prices = deque(maxlen=lookback_period + 1)
        self._position = 0  # Current position
        self._last_signal_price = None
        
    def _calculate_momentum(self) -> float:
        """Calculate price momentum (rate of change)."""
        if len(self._prices) < self._lookback_period + 1:
            return 0.0
            
        current_price = self._prices[-1]
        past_price = self._prices[0]
        
        if past_price == 0:
            return 0.0
            
        momentum = (current_price - past_price) / past_price
        return momentum
    
    def generate_signals(self, tick: MarketDataPoint) -> List[Tuple[str, str, int, float]]:
        """Generate signals based on momentum."""
        signals = []
        
        # Add new price to history
        self._prices.append(tick.price)
        
        # Calculate momentum
        momentum = self._calculate_momentum()
        
        # Avoid too frequent trading - only trade if price moved significantly
        price_change_threshold = 0.005  # 0.5%
        if (self._last_signal_price is not None and 
            abs(tick.price - self._last_signal_price) / self._last_signal_price < price_change_threshold):
            return signals
        
        # Generate signals based on momentum
        if momentum > self._momentum_threshold and self._position <= 0:
            # Strong positive momentum - buy
            if self._position == -1:
                # Close short position
                signals.append(('buy', tick.symbol, self._position_size, tick.price))
            # Open long position
            signals.append(('buy', tick.symbol, self._position_size, tick.price))
            self._position = 1
            self._last_signal_price = tick.price
            
        elif momentum < -self._momentum_threshold and self._position >= 0:
            # Strong negative momentum - sell
            if self._position == 1:
                # Close long position
                signals.append(('sell', tick.symbol, self._position_size, tick.price))
            # Open short position
            signals.append(('sell', tick.symbol, self._position_size, tick.price))
            self._position = -1
            self._last_signal_price = tick.price
            
        return signals


class BuyAndHoldStrategy(Strategy):
    """
    Simple Buy and Hold Strategy.
    
    Buys once at the beginning and holds throughout the backtest period.
    """
    
    def __init__(self, position_size: int = 100):
        """
        Initialize the buy and hold strategy.
        
        Args:
            position_size: Number of shares to buy and hold
        """
        self._position_size = position_size
        self._has_bought = False
        
    def generate_signals(self, tick: MarketDataPoint) -> List[Tuple[str, str, int, float]]:
        """Generate buy signal only once at the beginning."""
        if not self._has_bought:
            self._has_bought = True
            return [('buy', tick.symbol, self._position_size, tick.price)]
        return []