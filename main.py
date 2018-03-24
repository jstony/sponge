from sponge.scanner import Scanner
from sponge.opportunity import Opportunity
from sponge.symbol_pair import SymbolPair
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    scanner = Scanner()
    o = Opportunity(
        low_price_exchange='kraken',
        high_price_exchange='hitbtc2',
        estimated_fee=0.005,
        target_spread=0.01,
        symbol_pair=SymbolPair(
            source_symbol='USDT',
            target_symbol='ETH',
            source_symbol_alias={'kraken': 'USD'}
        ),
        interval=15,
    )

    scanner.add(o)
    scanner.start()
