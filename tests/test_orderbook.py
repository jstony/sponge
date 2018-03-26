from sponge.orderbook import OrderBook

raw_data = {'asks': [[498.91, 0.645], [499.33, 4.0], [499.34, 2.5], [499.35, 0.008], [499.51, 0.01]],
            'bids': [[498.53, 0.01], [498.52, 0.1], [498.51, 0.1], [498.42, 1.0], [498.37, 2.325]]}
orderbook = OrderBook(raw_data)


def test_asks():
    assert orderbook.asks == raw_data['asks']


def test_bids():
    assert orderbook.bids == raw_data['bids']


def test_ask_volume():
    assert orderbook.ask_volume(499.34) == 0.645 + 4.0 + 2.5


def test_bid_volume():
    assert orderbook.bid_volume(498.51) == 0.01 + 0.1 + 0.1


def test_best_ask_by_volume():
    assert orderbook.best_ask_by_volume(5) == 499.34
    assert orderbook.best_ask_by_volume(10) == 499.51


def best_bid_by_volume():
    assert orderbook.best_bid_by_volume(1) == 498.42
    assert orderbook.best_bid_by_volume(10) == 499.37
