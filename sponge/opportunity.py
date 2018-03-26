from typing import Union
import logging
from .orderbook import OrderBook
from .symbol_pair import SymbolPair
from .exchange import Exchange

log = logging.getLogger(__name__)


class Chance(object):
    def __init__(self, buy_price: float, buy_amount: float, sell_price: float, sell_amount: float):
        self.buy_price = buy_price
        self.buy_amount = buy_amount
        self.sell_price = sell_price
        self.sell_amount = sell_amount

    def __str__(self):
        return str(self.__dict__)


class Opportunity(object):
    """
    描述套利机会
    仅会判断 high_price_exchange 卖出，low_price_exchange 平仓的套利机会
    """

    def __init__(self,
                 low_price_exchange: Exchange,
                 high_price_exchange: Exchange,
                 estimated_fee: float,
                 target_spread: float,
                 least_amount: float,
                 symbol_pair: SymbolPair,
                 interval: int):
        self.low_price_exchange = low_price_exchange
        self.high_price_exchange = high_price_exchange
        if not 1 > estimated_fee > 0:
            raise ValueError("estimated_fee should be hundred percent value")
        self.estimated_fee = estimated_fee
        if not 1 > target_spread > 0:
            raise ValueError("target_spread should be hundred percent value")
        self.target_spread = target_spread
        self.least_amount = least_amount
        self.symbol_pair = symbol_pair
        self.interval = interval

    def chance(self, high_orderbook: OrderBook, low_orderbook: OrderBook) -> Union[Chance, None]:
        target_volume = self.least_amount * 2
        bid = high_orderbook.best_bid_by_volume(target_volume)
        ask = low_orderbook.best_ask_by_volume(target_volume)
        price_spread = bid - ask
        spread_rate = price_spread / min(bid, ask)
        profit_rate = spread_rate - self.estimated_fee
        log.info(
            "{symbol}: {low_exchange}(buy) {low_price} {high_exchange}(sell) {high_price} spread {spread:.2f}, rate {spread_rate:.2f}% fee {fee:.2f}% target_spread {target_spread:.2f}% -> profit:{profit_rate:.2f}% {action}".format(
                symbol=self.symbol_pair.get_pair_name(),
                low_exchange=self.low_price_exchange,
                high_exchange=self.high_price_exchange,
                low_price=ask,
                high_price=bid,
                spread_rate=spread_rate * 100,
                fee=self.estimated_fee * 100,
                target_spread=self.target_spread * 100,
                profit_rate=profit_rate * 100,
                spread=price_spread,
                action='DO' if profit_rate > self.target_spread else 'SKIP'))
        if profit_rate > self.target_spread:
            buy_amount = self.least_amount
            sell_amount = self.least_amount
            chance = Chance(buy_price=ask, buy_amount=buy_amount, sell_price=bid, sell_amount=sell_amount)
            log.info("PROFIT {}, detail: {}".format(price_spread * self.least_amount, chance))
            return chance
