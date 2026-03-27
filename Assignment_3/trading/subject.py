from typing import Protocol, List

class Observer(Protocol):
    def update(self, price: float) -> None:
        ...

class MarketDataSubject:
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
        pass

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
        pass

    def notify(self, price: float) -> None:
        for observer in self._observers:
            observer.update(price)
        pass