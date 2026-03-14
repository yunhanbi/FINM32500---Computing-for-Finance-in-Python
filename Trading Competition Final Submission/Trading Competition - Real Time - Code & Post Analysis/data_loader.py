import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
from models import MarketDataPoint

def data_loader(file_path):
    try:
        data = []

        with open(file_path, mode='r') as file:
            reader = csv.reader(file)

            # Read the header row
            header = next(reader, None)

            for row in reader:
                data.append(MarketDataPoint(
                    timestamp=datetime.fromisoformat(row[header.index('Datetime')]),
                    volume=float(row[header.index('Volume')]),
                    open=float(row[header.index('Open')]),
                    high=float(row[header.index('High')]),
                    low=float(row[header.index('Low')]),
                    close=float(row[header.index('Close')])
                )
                )
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
