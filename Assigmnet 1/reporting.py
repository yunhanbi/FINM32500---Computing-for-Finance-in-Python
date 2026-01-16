import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
from data_loader import data_loader
from engine import Engine
import numpy as np
import pandas as pd

def report(market_data, result):
    market_price = np.array([tick.price for tick in market_data]).reshape(-1, 1)
    final_report = np.hstack((result, market_price))
    final_df = pd.DataFrame(final_report, columns = ['PositionQuantity', 'AvgPrice', 'Return', 'Capital', 'MarketPrice'])
    final_df.to_csv('final_report.csv', index=False)
    return final_df