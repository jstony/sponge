from typing import Union
import logging
from .ohlc import OHLCPoint
from .symbol_pair import SymbolPair

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
                 low_price_exchange: str,
                 high_price_exchange: str,
                 estimated_fee: float,
                 target_spread: float,
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
        self.symbol_pair = symbol_pair
        self.interval = interval

    def chance(self, high_data: OHLCPoint, low_data: OHLCPoint) -> Union[Chance, None]:
        price_spread = high_data.close - low_data.close
        spread_rate = price_spread / low_data.close
        profit_rate = spread_rate - self.estimated_fee
        log.info(
            "{symbol}: {low_exchange}(buy) {low_price} {high_exchange}(sell) {high_price} spread {spread:.2f}, rate {spread_rate:.2f}% fee {fee:.2f}% target_spread {target_spread:.2f}% -> profit:{profit_rate:.2f}% {action}".format(
                symbol=self.symbol_pair.get_pair_name(),
                low_exchange=self.low_price_exchange,
                high_exchange=self.high_price_exchange,
                low_price=low_data.close,
                high_price=high_data.close,
                spread_rate=spread_rate * 100,
                fee=self.estimated_fee * 100,
                target_spread=self.target_spread * 100,
                profit_rate=profit_rate * 100,
                spread=high_data.close - low_data.close,
                action='DO' if profit_rate > self.target_spread else 'SKIP'))
        if profit_rate > self.target_spread:
            volume = min(low_data.volume, high_data.volume)
            buy_price = low_data.close
            buy_amount = volume
            sell_price = high_data.close
            sell_amount = volume
            chance = Chance(buy_price=buy_price, buy_amount=buy_amount, sell_price=sell_price, sell_amount=sell_amount)
            log.info("PROFIT {}, detail: {}".format((chance.sell_price - chance.buy_price) * volume, chance))
            return chance
