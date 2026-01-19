# main.py

"""
CSV-Based Algorithmic Trading Backtester
Main orchestration script that coordinates data loading, strategy execution, and reporting.
"""

import os
import sys
from typing import List

# Import our modules
from data_loader import load_market_data, generate_sample_data
from models import MarketDataPoint
from strategies import MovingAverageCrossoverStrategy, MomentumStrategy, BuyAndHoldStrategy
from engine import BacktestEngine
from reporting import generate_markdown_report, print_summary_stats


def main():
    """Main function that orchestrates the entire backtesting process."""
    
    print("CSV-Based Algorithmic Trading Backtester")
    print("="*50)
    
    # Configuration
    data_file = "market_data.csv"
    initial_cash = 100000.0
    commission = 1.0
    
    try:
        # Step 1: Ensure we have market data
        if not os.path.exists(data_file):
            print(f"Market data file '{data_file}' not found. Generating sample data...")
            generate_sample_data(data_file, num_ticks=500)
        
        # Step 2: Load market data
        print(f"\nLoading market data from {data_file}...")
        market_data = load_market_data(data_file)
        
        if not market_data:
            print("Error: No market data loaded!")
            return
        
        print(f"Loaded {len(market_data)} market data points")
        print(f"Data range: {market_data[0].timestamp} to {market_data[-1].timestamp}")
        print(f"Price range: ${min(d.price for d in market_data):.2f} to ${max(d.price for d in market_data):.2f}")
        
        # Step 3: Initialize backtesting engine
        print(f"\nInitializing backtesting engine...")
        engine = BacktestEngine(initial_cash=initial_cash, commission=commission)
        
        # Step 4: Add trading strategies
        print("Adding trading strategies...")
        
        # Moving Average Crossover Strategy
        ma_strategy = MovingAverageCrossoverStrategy(
            short_window=10, 
            long_window=20, 
            position_size=100
        )
        engine.add_strategy(ma_strategy)
        print(f"  ✓ Moving Average Crossover (10/20)")
        
        # Momentum Strategy
        momentum_strategy = MomentumStrategy(
            lookback_period=5,
            momentum_threshold=0.02,
            position_size=50
        )
        engine.add_strategy(momentum_strategy)
        print(f"  ✓ Momentum Strategy (5-period lookback)")
        
        # Buy and Hold Strategy (for comparison)
        buy_hold_strategy = BuyAndHoldStrategy(position_size=200)
        engine.add_strategy(buy_hold_strategy)
        print(f"  ✓ Buy and Hold Strategy")
        
        # Step 5: Run the backtest
        print(f"\nRunning backtest...")
        results = engine.run_backtest(market_data)
        
        # Step 6: Display results
        print_summary_stats(results)
        
        # Step 7: Generate detailed report
        print(f"\nGenerating detailed performance report...")
        generate_markdown_report(results, "performance.md")
        
        # Step 8: Display some key insights
        print(f"\nKey Insights:")
        print(f"  • Strategy achieved {results['total_return']*100:.2f}% total return")
        print(f"  • Sharpe ratio of {results['sharpe_ratio']:.3f}")
        print(f"  • Maximum drawdown: {results['max_drawdown']*100:.2f}%")
        print(f"  • Executed {results['successful_trades']} out of {results['total_trades']} trades successfully")
        
        if results['errors']:
            print(f"  • {len(results['errors'])} errors encountered (see performance.md for details)")
        
        print(f"\nDetailed report available in: performance.md")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure the market data file exists or check the file path.")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("Please check your data and configuration.")
        return 1
        
    print(f"\nBacktest completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())