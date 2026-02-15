from baseline import baseline
from optimization import optimization
from HeapSort_Opt import sort
import numpy as np
import pandas as pd
import time

def generate_input(len):
    input_df = pd.DataFrame(None)
    input_df['price'] = np.random.uniform(low=1.0, high=200.0, size=len)
    input_df['quantity'] = np.random.default_rng().integers(low=1.0, high=200.0, size=len)
    sides = ['bid', 'ask']
    input_df['side'] = np.random.choice(sides, size=len)
    input_df = input_df.reset_index(names=['order_id'])
    return input_df

orders = generate_input(10000)

base = baseline()
opt = optimization()
for idx in orders.index:
    base.add_order(orders.loc[idx, :].to_dict())
opt.add_order(orders)

# Queries in Naive Version
orders_by_id = { 6666:  order for order in base.asks + base.bids if order['order_id'] == 6666 }
price_levels = { 190: [order['order_id'] for order in base.asks + base.bids if round(order['price']) == 190 ] }
best_bid = base.bids[0]
best_ask = base.asks[0]

# Queries in Optimized Version
orders_by_id_opt = { 6666:  opt.orders_df.loc[6666,:].to_dict() }
price_levels_opt = { 190: opt.orders_df.loc[np.round(opt.orders_df['price']) == 190,'order_id'].to_list() }
best_bid_opt = sort(opt.orders_df.loc[opt.orders_df['side'] == 'bid', :], 'price', asc=False).iloc[0,:]
best_ask_opt = sort(opt.orders_df.loc[opt.orders_df['side'] == 'ask', :], 'price', asc=True).iloc[0,:]

