from typing import List
import logging
import time
from concurrent.futures import ThreadPoolExecutor, Executor
import ccxt
from .opportunity import Opportunity, Exchange
from .ohlc import OHLCPoint
from .orderbook import OrderBook

log = logging.getLogger(__name__)


class Scanner(object):
    def __init__(self):
        self.opportunities: List[Opportunity] = []
        self.executor: Executor = None

    def add(self, item: Opportunity):
        self.opportunities.append(item)

    def start(self):
        with ThreadPoolExecutor(max_workers=16) as executor:
            self.executor = executor
            while True:
                try:
                    self.scan_exchanges()
                except Exception as e:
                    log.error("error: {}, retry...".format(e))

    def scan_exchanges(self):
        for o in self.opportunities:
            self.watch(o)

    def watch(self, o: Opportunity):
        h_order_book_future = self.executor.submit(self.fetch_order_book, o.high_price_exchange, o)
        l_order_book_future = self.executor.submit(self.fetch_order_book, o.low_price_exchange, o)
        h_order_book: OrderBook = h_order_book_future.result()
        l_order_book: OrderBook = l_order_book_future.result()
        chance = o.chance(high_orderbook=h_order_book, low_orderbook=l_order_book)
        if not chance:
            pass
        time.sleep(o.interval)

    def fetch_ohlc(self, exchange: Exchange, opportunity: Opportunity) -> OHLCPoint:
        client = exchange.new_client()
        symbol = opportunity.symbol_pair.get_pair_name(exchange.name)
        raw_data = client.fetch_ohlcv(symbol=symbol, limit=1)
        return OHLCPoint(raw_data[0])

    def fetch_order_book(self, exchange: Exchange, opportunity: Opportunity) -> OrderBook:
        client = exchange.new_client()
        symbol = opportunity.symbol_pair.get_pair_name(exchange.name)
        raw_data = client.fetch_order_book(symbol=symbol, limit=50)
        return OrderBook(raw_data)
