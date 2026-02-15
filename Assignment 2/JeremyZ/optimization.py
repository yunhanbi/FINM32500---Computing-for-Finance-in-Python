import pandas as pd

class optimization:
    def __init__(self):
        data_type = {"order_id": int,
                     "price": float,
                     "quantity": int,
                     "side": object}
        self.orders_df = pd.DataFrame(columns=data_type.keys())
        self.orders_df = self.orders_df.astype(dtype=data_type)
        self.orders_df.set_index("order_id", drop=False, inplace=True)

    def add_order(self, orders):
        self.orders_df = pd.concat([self.orders_df, orders], ignore_index=True)
        self.orders_df.set_index("order_id", drop=False, inplace=True)

    def amend_order(self, order_ids, new_quantities):
        self.orders_df.loc[order_ids, 'quantity'] = new_quantities

    def delete_order(self, order_ids):
        self.orders_df.drop(order_ids, inplace=True)

