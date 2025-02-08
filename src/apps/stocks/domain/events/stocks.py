from dataclasses import dataclass
from domain.events.base import BaseEvent


@dataclass
class StockPriceUpdated(BaseEvent):
    stock_oid: str
    new_price: float
