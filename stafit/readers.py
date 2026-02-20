from csv import DictReader
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Sequence

from stafit.domain import EconomicRecord


class CsvEconomicDataReader:
    """Читает CSV-файлы и преобразует строки в EconomicRecord."""

    REQUIRED_COLUMNS = ("country", "gdp")

    def read_files(self, paths: Sequence[Path]) -> tuple[EconomicRecord, ...]:
        records: list[EconomicRecord] = []
        for path in paths:
            records.extend(self._read_file(path))
        return tuple(records)

    def _read_file(self, path: Path) -> tuple[EconomicRecord, ...]:
        with path.open("r", encoding="utf-8", newline="") as file:
            csv_reader = DictReader(file)
            fieldnames = csv_reader.fieldnames
            self._check_columns(path, fieldnames)
            return tuple(self._parse_row(path, row) for row in csv_reader)

    def _check_columns(self, path: Path, fieldnames: Sequence[str] | None) -> None:
        if not fieldnames:
            raise ValueError(f"Файл {path} пустой или не содержит заголовок.")

        missing_columns = tuple(
            column for column in self.REQUIRED_COLUMNS if column not in fieldnames
        )
        if missing_columns:
            columns_text = ", ".join(missing_columns)
            raise ValueError(f"Файл {path} не содержит колонки: {columns_text}.")

    @staticmethod
    def _parse_row(path: Path, row: dict[str, str | None]) -> EconomicRecord:
        country_value = row.get("country")
        country = country_value.strip() if country_value is not None else ""
        if not country:
            raise ValueError(f"Файл {path} содержит пустое значение country.")

        try:
            gdp = Decimal(row["gdp"] or "")
        except (InvalidOperation, KeyError, TypeError) as error:
            raise ValueError(f"Файл {path} содержит некорректный gdp.") from error

        return EconomicRecord(country=country, gdp=gdp)
