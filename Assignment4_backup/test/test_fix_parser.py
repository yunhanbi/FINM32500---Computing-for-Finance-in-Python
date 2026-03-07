import os
import sys
from trading.fix_parser import FixParser
import pytest
sys.path.append(os.path.dirname(os.getcwd()))

def test_fix_parser():
    parser = FixParser()

    assert parser.parse("8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128")['55'] == 'AAPL'
    assert len(parser.parse("8=FIX.4.2|35=D|55=AAPL|54=1|38=500|40=2|10=128")) == 7