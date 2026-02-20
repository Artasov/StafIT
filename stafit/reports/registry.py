from stafit.reports.average_gdp import AverageGdpReport
from stafit.reports.base import BaseReport


class ReportRegistry:
    """Реестр доступных отчетов."""

    def __init__(self) -> None:
        self._reports: dict[str, BaseReport] = {}

    def register(self, report: BaseReport) -> None:
        self._reports[report.name] = report

    def get(self, name: str) -> BaseReport:
        if name not in self._reports:
            available_reports = ", ".join(self.available_names())
            raise ValueError(f"Отчет '{name}' не найден. Доступны: {available_reports}.")
        return self._reports[name]

    def available_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._reports))

    @classmethod
    def with_default_reports(cls) -> "ReportRegistry":
        registry = cls()
        registry.register(AverageGdpReport())
        return registry
