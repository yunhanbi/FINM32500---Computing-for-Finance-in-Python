# Simple Trading Backtester

## Files
- `models.py` - MarketDataPoint (frozen), Order (mutable), exceptions
- `data_loader.py` - Load CSV into dataclasses
- `strategies.py` - Abstract Strategy + MovingAverage
- `engine.py` - Portfolio and BacktestEngine
- `reporting.py` - Generate performance report
- `main.py` - Run everything

## Run
```bash
python main.py
```

## Key Features
✅ Frozen dataclass (MarketDataPoint)
✅ Mutable class (Order)
✅ Abstract base class (Strategy)
✅ Custom exceptions (OrderError, ExecutionError)
✅ Exception handling (try/catch)
✅ Containers (lists, dicts)
