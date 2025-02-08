from dataclasses import dataclass

from domain.exceptions.base import ApplicationException

@dataclass(eq=False)
class InvalidStockSymbolException(ApplicationException):
    """Raised when an invalid stock symbol is provided."""
    symbol: str

    @property
    def message(self) -> str:
        return f"Invalid stock symbol: {self.symbol}"

class NegativeStockPriceException(ApplicationException):
    """Raised when a stock price is negative."""
    price: float

    @property
    def message(self) -> str:
        return f"Negative stock price: {self.price}"
