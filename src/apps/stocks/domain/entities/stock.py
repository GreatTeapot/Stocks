from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.stocks import StockPriceUpdated
from domain.values.stocks import StockSymbol, StockPrice


@dataclass(eq=False)
class Stock(BaseEntity):
    symbol: StockSymbol
    price: StockPrice

    def update_price(self, new_price: StockPrice) -> None:
        """Update the stock price and register a domain event."""
        if self.price.value != new_price.value:
            self.price = new_price
            self.register_event(StockPriceUpdated(stock_oid=self.oid, new_price=self.price.value))
