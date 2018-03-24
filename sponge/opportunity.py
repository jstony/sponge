from typing import Union
from dataclasses import dataclass
import logging
from .ohlc import OHLCPoint

log = logging.getLogger(__name__)


@dataclass
class Chance(object):
    buy_price: float
    buy_amount: float
    sell_price: float
    sell_amount: float


class Opportunity(object):
    """
    描述套利机会
    仅会判断 high_price_exchange 卖出，low_price_exchange 平仓的套利机会
    """

    def __init__(self, low_price_exchange: str, high_price_exchange: str, estimated_fee: float, target_spread: float,
                 source_symbol: str, target_symbol: str):
        self.low_price_exchange = low_price_exchange
        self.high_price_exchange = high_price_exchange
        if not 1 > estimated_fee > 0:
            raise ValueError("estimated_fee should be hundred percent value")
        self.estimated_fee = estimated_fee
        if not 1 > target_spread > 0:
            raise ValueError("target_spread should be hundred percent value")
        self.target_spread = target_spread
        self.symbol_pair = "{}/{}".format(target_symbol, source_symbol)

    def chance(self, high_data: OHLCPoint, low_data: OHLCPoint) -> Union[Chance, None]:
        price_spread = high_data.close - low_data.close
        spread_rate = price_spread / low_data.close
        profit_rate = spread_rate - self.estimated_fee
        log.info("check low {} high {} price {} {}, current_spread {} fee {} target_spread {} -> {} {}",
                 self.low_price_exchange, self.high_price_exchange,
                 low_data.close, high_data.close, spread_rate, self.estimated_fee, self.target_spread,
                 profit_rate, 'DO' if profit_rate > self.target_spread else 'SKIP')
        if profit_rate > self.target_spread:
            volume = min(low_data.volume, high_data.volume)
            buy_price = low_data.close
            buy_amount = volume
            sell_price = high_data.close
            sell_amount = volume
            chance = Chance(buy_price=buy_price, buy_amount=buy_amount, sell_price=sell_price, sell_amount=sell_amount)
            log.info("PROFIT {}, detail: {}", (chance.sell_amount - chance.buy_amount) * volume, chance)
            return chance
