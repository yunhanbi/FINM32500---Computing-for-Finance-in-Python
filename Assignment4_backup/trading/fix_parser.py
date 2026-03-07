import pandas as pd

class FixParser:
    def parse(self, msg):
        return dict(pd.Series(msg.split("|")).str.split(r'=').to_numpy())


