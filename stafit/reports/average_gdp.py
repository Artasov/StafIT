from decimal import Decimal, ROUND_HALF_UP
from typing import Sequence

from stafit.domain import EconomicRecord, ReportTable
from stafit.reports.base import BaseReport


class AverageGdpReport(BaseReport):
    """Отчет со средним ВВП по странам."""

    @property
    def name(self) -> str:
        return "average-gdp"

    def build(self, records: Sequence[EconomicRecord]) -> ReportTable:
        totals: dict[str, Decimal] = {}
        counts: dict[str, int] = {}
        for record in records:
            totals[record.country] = totals.get(record.country, Decimal("0")) + record.gdp
            counts[record.country] = counts.get(record.country, 0) + 1

        averages: list[tuple[str, Decimal]] = []
        for country, total in totals.items():
            average = (total / Decimal(counts[country])).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            averages.append((country, average))

        sorted_averages = sorted(averages, key=lambda row: (-row[1], row[0]))
        rows = tuple((country, f"{average:.2f}") for country, average in sorted_averages)
        return ReportTable(headers=("country", "average_gdp"), rows=rows)
