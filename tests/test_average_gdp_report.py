from decimal import Decimal

from stafit.domain import EconomicRecord
from stafit.reports.average_gdp import AverageGdpReport


class TestAverageGdpReport:
    def test_build_sorts_by_average_gdp_desc(self) -> None:
        records = (
            EconomicRecord(country="Germany", gdp=Decimal("4086")),
            EconomicRecord(country="Germany", gdp=Decimal("4072")),
            EconomicRecord(country="Germany", gdp=Decimal("4257")),
            EconomicRecord(country="United States", gdp=Decimal("25462")),
            EconomicRecord(country="United States", gdp=Decimal("23315")),
            EconomicRecord(country="United States", gdp=Decimal("22994")),
            EconomicRecord(country="China", gdp=Decimal("17963")),
            EconomicRecord(country="China", gdp=Decimal("17734")),
            EconomicRecord(country="China", gdp=Decimal("17734")),
        )

        report = AverageGdpReport()
        table = report.build(records)

        assert table.headers == ("country", "average_gdp")
        assert table.rows == (
            ("United States", "23923.67"),
            ("China", "17810.33"),
            ("Germany", "4138.33"),
        )

    def test_build_returns_only_headers_when_records_are_empty(self) -> None:
        report = AverageGdpReport()
        table = report.build(())

        assert table.headers == ("country", "average_gdp")
        assert table.rows == ()
