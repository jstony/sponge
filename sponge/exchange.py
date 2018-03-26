import ccxt


class Exchange(object):
    def __init__(self, name, config=None):
        self.name = name
        self.config = config

    def new_client(self) -> ccxt.Exchange:
        return getattr(ccxt, self.name)(config=self.config or {})

    def __str__(self):
        return self.name
