# data_loader.py

import csv
import datetime
from typing import List
from models import MarketDataPoint


def load_market_data(filename: str) -> List[MarketDataPoint]:
    """
    Load market data from CSV file into a list of MarketDataPoint objects.
    
    Args:
        filename: Path to the CSV file containing market data
        
    Returns:
        List of MarketDataPoint objects sorted by timestamp
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If data parsing fails
    """
    market_data = []
    
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 because of header
                try:
                    # Parse timestamp
                    timestamp_str = row['timestamp'].strip()
                    if 'T' in timestamp_str:
                        # ISO format with T separator
                        timestamp = datetime.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    else:
                        # Try common formats
                        try:
                            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                        except ValueError:
                            timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    
                    # Parse symbol and price
                    symbol = row['symbol'].strip()
                    price = float(row['price'])
                    
                    # Create MarketDataPoint
                    data_point = MarketDataPoint(
                        timestamp=timestamp,
                        symbol=symbol,
                        price=price
                    )
                    
                    market_data.append(data_point)
                    
                except (ValueError, KeyError) as e:
                    print(f"Warning: Failed to parse row {row_num}: {row}. Error: {e}")
                    continue
                    
    except FileNotFoundError:
        raise FileNotFoundError(f"Market data file '{filename}' not found")
    
    # Sort by timestamp to ensure chronological order
    market_data.sort(key=lambda x: x.timestamp)
    
    print(f"Loaded {len(market_data)} market data points from {filename}")
    return market_data


def generate_sample_data(filename: str = "market_data.csv", num_ticks: int = 500) -> None:
    """
    Generate sample market data CSV file for testing.
    
    Args:
        filename: Name of the output CSV file
        num_ticks: Number of market data ticks to generate
    """
    import random
    
    base_time = datetime.datetime(2024, 1, 1, 9, 30, 0)  # Market open
    current_price = 150.0
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'symbol', 'price'])
        
        for i in range(num_ticks):
            # Generate timestamp (1 minute intervals)
            timestamp = base_time + datetime.timedelta(minutes=i)
            
            # Random walk price movement
            price_change = random.gauss(0, 0.02)  # 2% volatility
            current_price *= (1 + price_change)
            current_price = round(current_price, 2)
            
            writer.writerow([timestamp.isoformat(), 'AAPL', current_price])
    
    print(f"Generated sample data file '{filename}' with {num_ticks} ticks")


if __name__ == "__main__":
    # Generate sample data if no file exists
    import os
    
    filename = "market_data.csv"
    if not os.path.exists(filename):
        generate_sample_data(filename)
    
    # Test loading the data
    try:
        data = load_market_data(filename)
        print(f"Successfully loaded {len(data)} data points")
        if data:
            print(f"First point: {data[0]}")
            print(f"Last point: {data[-1]}")
    except Exception as e:
        print(f"Error loading data: {e}")