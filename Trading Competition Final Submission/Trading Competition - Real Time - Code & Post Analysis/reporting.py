import csv
from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import datetime
from data_loader import data_loader
from engine import Engine
import numpy as np
import pandas as pd

def report(result, symbol):
    final_df = pd.DataFrame(result, columns = ['PositionQuantity', 'AvgPrice', 'Return', 'Capital', 'TimeStamp', 'MarketPrice'])
    final_df.to_csv(rf'final_report_{symbol}.csv', index=False)
    return final_df