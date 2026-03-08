import yfinance as yf

df = yf.download(tickers='GOOG', period='8d', interval='1m')
df.columns = df.columns.droplevel(1)
df = df.reset_index(drop=False)

df.to_csv('market_data_GOOG.csv', index=False)

# import numpy as np
#
# arr = np.empty((0,3))
# arr = np.append(arr, [[1,2,3]], axis=0)
# arr = np.append(arr, [[4,5,6]], axis=0)
# print(np.append(arr, [[7,7,7]], axis=0)[:-1,0])