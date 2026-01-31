class baseline:
    def __init__(self):
        self.bids = []
        self.asks = []

    def add_order(self, order_dict):
        try:
            if order_dict['side'] == 'bid':
                self.bids.append(order_dict)
                self.bids = sorted(self.bids, key=lambda x: x['price'], reverse=True)
            elif order_dict['side'] == 'ask':
                self.asks.append(order_dict)
                self.asks = sorted(self.asks, key=lambda x: x['price'], reverse=False)
            else:
                raise ValueError('Invalid side')

        except Exception as err:
            raise err

    def amend_order(self, order_id, new_quantity):
        
        for index, bid in enumerate(self.bids):
            if order_id == bid['order_id']:
                self.bids[index]['quantity'] = new_quantity

        for index, ask in enumerate(self.asks):
            if order_id == ask['order_id']:
                self.asks[index]['quantity'] = new_quantity

        self.bids = sorted(self.bids, key=lambda x: x['price'], reverse=True)
        self.asks = sorted(self.asks, key=lambda x: x['price'], reverse=False)

    def delete_order(self, order_id):

        for index, bid in enumerate(self.bids):
            if order_id == bid['order_id']:
                self.bids.pop(index)

        for index, ask in enumerate(self.asks):
            if order_id == ask['order_id']:
                self.asks.pop(index)

        self.bids = sorted(self.bids, key=lambda x: x['price'], reverse=True)
        self.asks = sorted(self.asks, key=lambda x: x['price'], reverse=False)

