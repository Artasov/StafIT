from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class EconomicRecord:
    country: str
    gdp: Decimal


@dataclass(frozen=True)
class ReportTable:
    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]
