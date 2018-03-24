import typing
import arrow


class OHLCPoint(object):
    def __init__(self, data: typing.List[float]):
        self._data = data

    @property
    def empty(self) -> bool:
        return len(self._data) == 0

    @property
    def timestamp(self) -> arrow.Arrow:
        return arrow.get(self._data[0] / 1000)

    @property
    def open(self) -> float:
        return self._data[1]

    @property
    def high(self) -> float:
        return self._data[2]

    @property
    def low(self) -> float:
        return self._data[3]

    @property
    def close(self) -> float:
        return self._data[4]

    @property
    def volume(self) -> float:
        return self._data[5]

    def __str__(self):
        return str(self._data)
