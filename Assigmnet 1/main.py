import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
from data_loader import data_loader
from engine import Engine
from reporting import report
import numpy as np

file_path = 'market_data.csv'
capital = 10000
risk = 1000
stop = 0.03
market_data = data_loader(file_path)

def main():
    market_data = data_loader(file_path)
    result = Engine(risk, stop, market_data, capital).execute()
    print(report(market_data, result))

if __name__ == '__main__':
    main()