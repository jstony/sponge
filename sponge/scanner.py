from typing import List
import logging
import ccxt as ccxt
from .ohlc import OHLCPoint
from .opportunity import Opportunity

log = logging.getLogger(__name__)


class Scanner(object):
    def __init__(self):
        self.opportunities: List[Opportunity] = []

    def add(self, item: Opportunity):
        self.opportunities.append(item)

    def start(self):
        while True:
            self.fetch_exchanges_ticker()

    def fetch_exchanges_ticker(self):
        for opportunity in self.opportunities:
            h_client: ccxt.Exchange = getattr(ccxt, opportunity.high_price_exchange)
            l_client: ccxt.Exchange = getattr(ccxt, opportunity.low_price_exchange)
            h_data = OHLCPoint(h_client.fetch_ohlcv(opportunity.symbol_pair, limit=1)[0])
            l_data = OHLCPoint(l_client.fetch_ohlcv(opportunity.symbol_pair, limit=1)[0])
            chance = opportunity.chance(high_data=h_data, low_data=l_data)
            if chance:
                pass  # buy
