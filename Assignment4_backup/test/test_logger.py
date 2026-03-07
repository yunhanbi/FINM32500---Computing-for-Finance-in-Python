import os
import sys
import json
sys.path.append(os.path.dirname(os.getcwd()))
from trading.logger import Logger
import pytest


def test_log():
    logger = Logger()
    logger.log('test', '1')

    assert logger.logs == [['[LOG] test -> 1']]

def test_save():
    logger = Logger()
    logger.log('test', '1')
    logger.log('test', '2')
    logger.save('test.json')
    with open('test.json', 'r') as file:
        data = json.load(file)
    assert data == [['[LOG] test -> 1'], ['[LOG] test -> 2']]