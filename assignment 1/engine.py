# engine.py

import random
from typing import List, Dict, Tuple
import datetime
from models import MarketDataPoint, Order, Position, OrderError, ExecutionError
from strategies import Strategy


class BacktestEngine:
    """
    Main backtesting engine that orchestrates strategy execution and order management.
    """
    
    def __init__(self, initial_cash: float = 100000.0, commission: float = 1.0):
        """
        Initialize the backtesting engine.
        
        Args:
            initial_cash: Starting cash amount
            commission: Commission per trade
        """
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.commission = commission
        
        # Portfolio management
        self.positions: Dict[str, Position] = {}
        self.orders: List[Order] = []
        self.executed_orders: List[Order] = []
        self.failed_orders: List[Order] = []
        
        # Performance tracking
        self.portfolio_values = []
        self.timestamps = []
        self.trades = []
        
        # Error logging
        self.errors = []
        
        # Strategies
        self.strategies: List[Strategy] = []
        
    def add_strategy(self, strategy: Strategy) -> None:
        """Add a trading strategy to the engine."""
        self.strategies.append(strategy)
        
    def _create_order(self, action: str, symbol: str, quantity: int, 
                     price: float, timestamp: datetime.datetime) -> Order:
        """
        Create and validate an order.
        
        Args:
            action: 'buy' or 'sell'
            symbol: Trading symbol
            quantity: Number of shares
            price: Order price
            timestamp: Order timestamp
            
        Returns:
            Validated Order object
            
        Raises:
            OrderError: If order parameters are invalid
        """
        # Convert action to signed quantity
        if action.lower() == 'buy':
            signed_quantity = abs(quantity)
        elif action.lower() == 'sell':
            signed_quantity = -abs(quantity)
        else:
            raise OrderError(f"Invalid order action: {action}")
            
        # Create order
        order = Order(
            symbol=symbol,
            quantity=signed_quantity,
            price=price,
            timestamp=timestamp
        )
        
        return order
    
    def _execute_order(self, order: Order, current_price: float) -> bool:
        """
        Execute an order and update portfolio.
        
        Args:
            order: Order to execute
            current_price: Current market price
            
        Returns:
            True if execution successful, False otherwise
        """
        try:
            # Simulate occasional execution failures
            if random.random() < 0.02:  # 2% failure rate
                raise ExecutionError(f"Simulated execution failure for order {order}")
            
            # Check if we have enough cash for buy orders
            if order.quantity > 0:  # Buy order
                cost = order.quantity * current_price + self.commission
                if cost > self.cash:
                    raise ExecutionError(f"Insufficient funds for order {order}")
                    
                # Update cash
                self.cash -= cost
                
            else:  # Sell order
                # Check if we have enough shares to sell
                symbol_position = self.positions.get(order.symbol)
                if symbol_position is None or symbol_position.quantity < abs(order.quantity):
                    # Allow short selling but log it
                    pass
                    
                # Update cash
                proceeds = abs(order.quantity) * current_price - self.commission
                self.cash += proceeds
            
            # Update position
            if order.symbol not in self.positions:
                self.positions[order.symbol] = Position(symbol=order.symbol)
                
            self.positions[order.symbol].update_position(order.quantity, current_price)
            
            # Record trade
            trade = {
                'timestamp': order.timestamp,
                'symbol': order.symbol,
                'action': 'buy' if order.quantity > 0 else 'sell',
                'quantity': abs(order.quantity),
                'price': current_price,
                'cash_after': self.cash
            }
            self.trades.append(trade)
            
            # Update order status
            order.update_status('filled')
            self.executed_orders.append(order)
            
            return True
            
        except (OrderError, ExecutionError) as e:
            # Log error and mark order as failed
            error_msg = f"Order execution failed: {e}"
            self.errors.append({
                'timestamp': order.timestamp,
                'error': error_msg,
                'order': order
            })
            
            order.update_status('rejected')
            self.failed_orders.append(order)
            
            return False
    
    def _calculate_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """Calculate total portfolio value including cash and positions."""
        total_value = self.cash
        
        for symbol, position in self.positions.items():
            if position.quantity != 0:
                current_price = current_prices.get(symbol, 0.0)
                position_value = position.quantity * current_price
                total_value += position_value
                
                # Update unrealized P&L
                position.calculate_unrealized_pnl(current_price)
        
        return total_value
    
    def run_backtest(self, market_data: List[MarketDataPoint]) -> Dict:
        """
        Run the backtest on the provided market data.
        
        Args:
            market_data: List of MarketDataPoint objects in chronological order
            
        Returns:
            Dictionary containing backtest results
        """
        print(f"Starting backtest with {len(market_data)} data points...")
        print(f"Initial cash: ${self.initial_cash:,.2f}")
        print(f"Active strategies: {len(self.strategies)}")
        
        current_prices = {}
        
        for i, tick in enumerate(market_data):
            try:
                # Update current prices
                current_prices[tick.symbol] = tick.price
                
                # Generate signals from all strategies
                all_signals = []
                for strategy in self.strategies:
                    try:
                        signals = strategy.generate_signals(tick)
                        all_signals.extend(signals)
                    except Exception as e:
                        error_msg = f"Strategy error: {e}"
                        self.errors.append({
                            'timestamp': tick.timestamp,
                            'error': error_msg,
                            'strategy': strategy.__class__.__name__
                        })
                
                # Process signals and create orders
                for signal in all_signals:
                    try:
                        action, symbol, quantity, price = signal
                        order = self._create_order(action, symbol, quantity, price, tick.timestamp)
                        self.orders.append(order)
                        
                        # Execute order
                        self._execute_order(order, tick.price)
                        
                    except (OrderError, ExecutionError) as e:
                        error_msg = f"Signal processing error: {e}"
                        self.errors.append({
                            'timestamp': tick.timestamp,
                            'error': error_msg,
                            'signal': signal
                        })
                
                # Calculate and record portfolio value
                portfolio_value = self._calculate_portfolio_value(current_prices)
                self.portfolio_values.append(portfolio_value)
                self.timestamps.append(tick.timestamp)
                
                # Progress reporting
                if (i + 1) % 100 == 0:
                    print(f"Processed {i + 1}/{len(market_data)} ticks. "
                          f"Portfolio value: ${portfolio_value:,.2f}")
                    
            except Exception as e:
                error_msg = f"Unexpected error processing tick {i}: {e}"
                self.errors.append({
                    'timestamp': tick.timestamp,
                    'error': error_msg,
                    'tick': tick
                })
                continue
        
        # Calculate final results
        results = self._calculate_results()
        
        print(f"Backtest completed!")
        print(f"Final portfolio value: ${results['final_value']:,.2f}")
        print(f"Total return: {results['total_return']:.2%}")
        print(f"Total trades: {len(self.trades)}")
        print(f"Failed orders: {len(self.failed_orders)}")
        print(f"Errors encountered: {len(self.errors)}")
        
        return results
    
    def _calculate_results(self) -> Dict:
        """Calculate comprehensive backtest results."""
        if not self.portfolio_values:
            return {'error': 'No portfolio values calculated'}
        
        final_value = self.portfolio_values[-1]
        total_return = (final_value - self.initial_cash) / self.initial_cash
        
        # Calculate periodic returns
        returns = []
        for i in range(1, len(self.portfolio_values)):
            ret = (self.portfolio_values[i] - self.portfolio_values[i-1]) / self.portfolio_values[i-1]
            returns.append(ret)
        
        # Calculate Sharpe ratio (assuming 252 trading days per year)
        if returns:
            avg_return = sum(returns) / len(returns)
            return_std = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
            sharpe_ratio = (avg_return * 252) / (return_std * (252 ** 0.5)) if return_std > 0 else 0
        else:
            sharpe_ratio = 0
            
        # Calculate maximum drawdown
        max_drawdown = 0
        peak_value = self.initial_cash
        for value in self.portfolio_values:
            if value > peak_value:
                peak_value = value
            drawdown = (peak_value - value) / peak_value
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        results = {
            'initial_value': self.initial_cash,
            'final_value': final_value,
            'total_return': total_return,
            'returns': returns,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': len(self.trades),
            'successful_trades': len(self.executed_orders),
            'failed_trades': len(self.failed_orders),
            'total_errors': len(self.errors),
            'portfolio_values': self.portfolio_values,
            'timestamps': self.timestamps,
            'trades': self.trades,
            'positions': self.positions,
            'errors': self.errors
        }
        
        return results