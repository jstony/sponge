from typing import List
import logging
import time
import ccxt as ccxt
from .opportunity import Opportunity

log = logging.getLogger(__name__)


class Scanner(object):
    def __init__(self):
        self.opportunities: List[Opportunity] = []

    def add(self, item: Opportunity):
        self.opportunities.append(item)

    def start(self):
        while True:
            try:
                self.fetch_exchanges_ticker()
            except Exception as e:
                log.error("error: {}, retry...".format(e))

    def fetch_exchanges_ticker(self):
        for opportunity in self.opportunities:
            h_client: ccxt.Exchange = getattr(ccxt, opportunity.high_price_exchange)()
            l_client: ccxt.Exchange = getattr(ccxt, opportunity.low_price_exchange)()
            h_data = opportunity.fetch_high_price_ohlc(h_client)
            l_data = opportunity.fetch_low_price_ohlc(l_client)
            chance = opportunity.chance(high_data=h_data, low_data=l_data)
            if chance:
                pass  # buy
            time.sleep(opportunity.interval)
