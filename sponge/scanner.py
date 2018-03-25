from typing import List
import logging
import time
from concurrent.futures import ThreadPoolExecutor, Executor
import ccxt
from .opportunity import Opportunity
from .ohlc import OHLCPoint

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
        fs = [self.executor.submit(self.watch, o) for o in self.opportunities]
        for f in fs:
            f.result()

    def watch(self, opportunity: Opportunity):
        h_client: ccxt.Exchange = getattr(ccxt, opportunity.high_price_exchange)()
        l_client: ccxt.Exchange = getattr(ccxt, opportunity.low_price_exchange)()
        h_data_future = self.executor.submit(self.fetch_ohlc, h_client, opportunity)
        l_data_future = self.executor.submit(self.fetch_ohlc, l_client, opportunity)
        chance = opportunity.chance(high_data=h_data_future.result(), low_data=l_data_future.result())
        if chance:
            pass  # buy
        time.sleep(opportunity.interval)

    def fetch_ohlc(self, client: ccxt.Exchange, opportunity: Opportunity) -> OHLCPoint:
        symbol = opportunity.symbol_pair.get_pair_name(client.describe()['id'])
        raw_data = client.fetch_ohlcv(symbol=symbol, limit=1)
        return OHLCPoint(raw_data[0])
