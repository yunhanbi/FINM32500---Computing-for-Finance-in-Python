from data_loader import load_market_data
from strategies import MovingAverageStrategy
from engine import BacktestEngine
from reporting import save_report

# Load data
market_data = load_market_data('market_data.csv')

# Create strategy
strategy = MovingAverageStrategy()

# Run backtest
engine = BacktestEngine([strategy])
portfolio = engine.run(market_data)

# Generate report
save_report(portfolio)

print(f"Final Cash: ${portfolio.cash:,.2f}")
print(f"Trades: {len(portfolio.history)}")
print(f"Errors: {len(engine.errors)}")
