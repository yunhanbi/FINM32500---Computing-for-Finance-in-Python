import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))

from ..trading.subject import MarketDataSubject
from unittest.mock import MagicMock

def test_attach_and_notify_calls_update():
    subject = MarketDataSubject()
    obs = MagicMock()
    subject.attach(obs)

    subject.notify(101.0)

    obs.update.assert_called_once_with(101.0)

def test_detach_stops_notifications():
    subject = MarketDataSubject()
    obs = MagicMock()
    subject.attach(obs)
    subject.detach(obs)

    subject.notify(101.0)

    obs.update.assert_not_called()
