from abc import ABC, abstractmethod
from typing import Sequence

from stafit.domain import EconomicRecord, ReportTable


class BaseReport(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def build(self, records: Sequence[EconomicRecord]) -> ReportTable:
        raise NotImplementedError
