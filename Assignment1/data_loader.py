import csv
from datetime import datetime
from models import MarketDataPoint

def load_market_data(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(MarketDataPoint(
                timestamp=datetime.fromisoformat(row['timestamp']),
                symbol=row['symbol'],
                price=float(row['price'])
            ))
    return data
