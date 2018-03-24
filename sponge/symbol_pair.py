from typing import Dict, Optional

SymbolAlias = Dict[str, str]


class SymbolPair(object):
    def __init__(self, source_symbol: str, target_symbol: str,
                 source_symbol_alias: SymbolAlias = None,
                 target_symbol_alias: SymbolAlias = None):
        self._source_symbol = source_symbol
        self._target_symbol = target_symbol
        self.source_symbol_alias = source_symbol_alias or dict()
        self.target_symbol_alias = target_symbol_alias or dict()

    def get_source_symbol(self, exchange: Optional[str] = None) -> str:
        return self.source_symbol_alias.get(exchange, self._source_symbol)

    def get_target_symbol(self, exchange: Optional[str] = None) -> str:
        return self.target_symbol_alias.get(exchange, self._target_symbol)

    def get_pair_name(self, exchange: Optional[str] = None) -> str:
        return "{}/{}".format(self.get_target_symbol(exchange), self.get_source_symbol(exchange))

    def __str__(self):
        return self.get_pair_name()
