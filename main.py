from sponge.scanner import Scanner
from sponge.opportunity import Opportunity

if __name__ == '__main__':
    scanner = Scanner()
    o = Opportunity(
        low_price_exchange='kraken',
        high_price_exchange='hitbtc',
        estimated_fee=0.01,
        target_spread=0.01,
        source_symbol='USD',
        target_symbol='ETC',
    )
    scanner.add(o)
    scanner.start()
