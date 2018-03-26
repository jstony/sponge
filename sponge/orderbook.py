from typing import List

RawDataRow = List[List[float]]


class OrderBook(object):
    def __init__(self, raw_data):
        self._raw_data = raw_data

    @property
    def asks(self) -> RawDataRow:
        return self._raw_data['asks']

    @property
    def bids(self) -> RawDataRow:
        return self._raw_data['bids']

    def ask_volume(self, max_price: float) -> float:
        return sum([volume for price, volume in self.asks if price <= max_price])

    def bid_volume(self, min_price: float) -> float:
        return sum([volume for price, volume in self.bids if price >= min_price])

    def best_bid_by_volume(self, target_volume: float) -> float:
        total_volume = 0
        last_price = 0
        for price, volume in self.bids:
            last_price = price
            total_volume += volume
            if total_volume >= target_volume:
                break

        return last_price

    def best_ask_by_volume(self, target_volume: float) -> float:
        total_volume = 0
        last_price = 0
        for price, volume in self.asks:
            last_price = price
            total_volume += volume
            if total_volume >= target_volume:
                break

        return last_price
