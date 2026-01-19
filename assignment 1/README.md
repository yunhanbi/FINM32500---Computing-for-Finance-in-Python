# CSV-Based Algorithmic Trading Backtester

A comprehensive Python backtesting framework that reads market data from CSV files, applies trading strategies, executes simulated orders, and produces detailed performance reports. This project demonstrates advanced Python concepts including object-oriented design, exception handling, and financial analytics.

## Learning Objectives Demonstrated

**Parse CSV data into immutable dataclass instances**
- Implemented frozen `MarketDataPoint` dataclass for type-safe market data
- Built robust CSV parser with datetime handling and error recovery

**Distinguish and use mutable classes for order management**  
- Created mutable `Order` class with updateable status and attributes
- Demonstrated mutability vs immutability in unit tests

**Build abstract Strategy interface with concrete subclasses**
- Abstract `Strategy` base class with `@abstractmethod generate_signals`
- Three concrete implementations: Moving Average, Momentum, Buy-and-Hold

**Manage time-series data and portfolio state using lists and dictionaries**
- Market data in chronological list structures
- Portfolio positions tracked in symbol-keyed dictionaries
- Signal aggregation and portfolio value time series

**Define custom exceptions and handle errors without stopping backtest**
- Custom `OrderError` and `ExecutionError` exception classes  
- Graceful error handling with continued processing and logging

**Generate Markdown report with key performance metrics**
- Comprehensive report with tables, charts, and narrative analysis
- Financial metrics: Sharpe ratio, maximum drawdown, risk analysis

## Project Structure

```
finm32500-python/
│
├── Data Management
│   ├── data_loader.py          # CSV parsing and data ingestion
│   ├── data_generator.py       # Sample data generation utilities
│   └── market_data.csv         # Sample market data file
│
├── Core Models
│   ├── models.py               # MarketDataPoint, Order, Position classes
│   └── strategies.py           # Strategy interface and implementations
│
├── Execution Engine
│   ├── engine.py               # BacktestEngine orchestration
│   └── main.py                 # Main entry point script
│
├── Analytics & Reporting
│   ├── reporting.py            # Performance analysis and report generation
│   ├── performance_report.md   # Generated performance report
│   └── assignment1.ipynb       # Interactive analysis notebook
│
└── Documentation
    └── README.md               # This file
```

## Quick Start

### Prerequisites
- Python 3.7+ with standard library (no external dependencies required!)
- VS Code or Jupyter for notebook execution

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   # Ensure all Python files are in the same directory
   ```

2. **Generate sample data** (if needed)
   ```python
   python data_generator.py
   ```

3. **Run the backtester**
   ```python
   python main.py
   ```

4. **Explore results in Jupyter**
   ```python
   # Open assignment1.ipynb for interactive analysis
   # Follow the notebook cells sequentially
   ```

### Alternative Execution Methods

**Method 1: Command Line**
```bash
cd finm32500-python
python main.py
```

**Method 2: Interactive Notebook**
- Open `assignment1.ipynb` in VS Code or Jupyter
- Execute cells sequentially for step-by-step analysis

**Method 3: Module Import**
```python
from main import main
results = main()
```

## Module Descriptions

### Core Components

**`models.py`** - Data Models and Exceptions
- `MarketDataPoint`: Frozen dataclass for immutable market data
- `Order`: Mutable class for trade order management  
- `Position`: Portfolio position tracking
- `OrderError`, `ExecutionError`: Custom exception classes

**`strategies.py`** - Trading Strategy Framework
- `Strategy`: Abstract base class with polymorphic interface
- `MovingAverageCrossoverStrategy`: Technical analysis with MA crossovers
- `MomentumStrategy`: Price momentum-based signals
- `BuyAndHoldStrategy`: Baseline buy-and-hold benchmark

**`engine.py`** - Backtesting Orchestration
- `BacktestEngine`: Main execution coordinator
- Order validation, execution simulation, and error handling
- Portfolio state management and performance tracking

### Data & Analytics

**`data_loader.py`** - Market Data Management
- CSV file parsing with robust error handling
- Automatic data type conversion and validation
- Sample data generation utilities

**`reporting.py`** - Performance Analytics
- Financial metrics calculation (Sharpe ratio, drawdown)
- Comprehensive Markdown report generation
- ASCII equity curve visualization
- Risk analysis and strategic insights

**`main.py`** - Application Entry Point
- Complete workflow orchestration
- Configuration management
- Console output and progress reporting

## Trading Strategies Explained

### 1. Moving Average Crossover
- **Logic**: Buy when short MA crosses above long MA, sell on reverse
- **Parameters**: `short_window=10`, `long_window=20`, `position_size=100`
- **Use Case**: Trend-following strategy for trending markets

### 2. Momentum Strategy  
- **Logic**: Buy on strong positive momentum, sell on negative
- **Parameters**: `lookback_period=5`, `momentum_threshold=0.02`
- **Use Case**: Captures short-term price acceleration

### 3. Buy and Hold Baseline
- **Logic**: Single purchase at start, hold throughout period
- **Parameters**: `position_size=200`
- **Use Case**: Benchmark for active strategy comparison

## Performance Metrics

The backtester calculates comprehensive performance statistics:

### Return Metrics
- **Total Return**: Overall portfolio performance percentage
- **Periodic Returns**: Time-series of period-over-period returns
- **Annualized Return**: Scaled annual performance estimate

### Risk Metrics  
- **Sharpe Ratio**: Risk-adjusted return measurement
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Volatility**: Annualized return standard deviation
- **Win Rate**: Percentage of profitable trades

### Operational Metrics
- **Trade Count**: Total number of executed orders
- **Success Rate**: Percentage of successfully executed orders
- **Error Rate**: System reliability and error handling effectiveness

## Testing & Validation

The project includes comprehensive testing via the Jupyter notebook:

### Unit Tests
- MarketDataPoint immutability verification
- Order mutability and status updates
- Exception raising and handling
- Strategy signal generation

### Integration Tests  
- End-to-end backtesting workflow
- Data loading and validation
- Multi-strategy execution
- Error resilience under simulated failures

### Performance Validation
- Financial metrics calculation accuracy
- Portfolio state consistency
- Report generation completeness

## Output Files

After running the backtester, you'll find:

1. **`market_data.csv`** - Generated sample market data
2. **`performance_report.md`** - Comprehensive analysis report
3. **Console output** - Real-time progress and summary statistics
4. **Notebook results** - Interactive analysis in `assignment1.ipynb`

## Technical Highlights

### Advanced Python Concepts
- **Abstract Base Classes**: Polymorphic strategy interface
- **Dataclasses**: Type-safe immutable data structures  
- **Exception Handling**: Custom exception hierarchy
- **List/Dict Management**: Complex container operations
- **Context Management**: File I/O with proper resource handling

### Financial Engineering
- **Time Series Analysis**: Chronological data processing
- **Risk Management**: Position sizing and portfolio tracking
- **Performance Attribution**: Strategy contribution analysis
- **Market Simulation**: Realistic execution modeling

### Software Engineering  
- **Modular Design**: Separation of concerns across modules
- **Error Resilience**: Graceful degradation under failures
- **Documentation**: Comprehensive inline and external docs
- **Testing**: Unit and integration test coverage

## Future Enhancement Opportunities

1. **Multi-Asset Support**: Extend to portfolios with multiple symbols
2. **Advanced Strategies**: Machine learning and statistical arbitrage
3. **Risk Management**: Stop-loss and position sizing rules  
4. **Market Simulation**: More realistic transaction costs and slippage
5. **Visualization**: Interactive charts with matplotlib/plotly
6. **Database Integration**: PostgreSQL or MongoDB for data storage
7. **Real-Time Data**: Integration with market data APIs
8. **Web Interface**: Flask/FastAPI dashboard for results

## Educational Value

This project serves as an excellent demonstration of:
- **Object-Oriented Programming**: Inheritance, polymorphism, encapsulation
- **Financial Programming**: Trading logic and performance analysis
- **Error Handling**: Robust exception management
- **Data Structures**: Effective use of Python containers
- **Documentation**: Professional code documentation practices
- **Testing**: Comprehensive validation methodologies

## Support & Issues

For questions about the implementation or to report issues:
1. Review the comprehensive notebook analysis in `assignment1.ipynb`
2. Check the generated performance report for detailed metrics
3. Examine console output for real-time execution feedback
4. Refer to inline code documentation for technical details

---

**Created by**: CSV-Based Algorithmic Trading Backtester  
**Course**: FINM 32500 Python Programming  
**Completed**: January 2026

*This project demonstrates mastery of advanced Python programming concepts applied to quantitative finance and algorithmic trading.*