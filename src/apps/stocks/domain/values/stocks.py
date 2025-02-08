from dataclasses import dataclass

from domain.exceptions.stocks.exceptions import InvalidStockSymbolException, NegativeStockPriceException
from domain.values.base import BaseValueObject
import re


@dataclass(frozen=True)
class StockSymbol(BaseValueObject):
    def validate(self):
        """Ensure stock symbol is valid (e.g., 'AAPL', 'GOOGL')."""
        if not re.match(r"^[A-Z]{1,5}$", self.value):
            raise InvalidStockSymbolException(f"Invalid stock symbol: {self.value}")


@dataclass(frozen=True)
class StockPrice(BaseValueObject):
    def validate(self):
        """Ensure stock price is non-negative."""
        if self.value < 0:
            raise NegativeStockPriceException()
