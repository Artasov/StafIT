from pathlib import Path

import pytest

from stafit.readers import CsvEconomicDataReader


class TestCsvEconomicDataReader:
    @staticmethod
    def _write_csv(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8", newline="")

    def test_read_files_returns_records_from_all_files(self, tmp_path: Path) -> None:
        first_file = tmp_path / "first.csv"
        second_file = tmp_path / "second.csv"
        self._write_csv(
            first_file,
            (
                "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
                "United States,2023,25462,2.1,3.4,3.7,339,North America\n"
            ),
        )
        self._write_csv(
            second_file,
            (
                "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
                "China,2023,17963,5.2,2.5,5.2,1425,Asia\n"
            ),
        )

        reader = CsvEconomicDataReader()
        records = reader.read_files((first_file, second_file))

        assert len(records) == 2
        assert records[0].country == "United States"
        assert records[1].country == "China"

    def test_read_files_raises_error_when_required_column_is_missing(
            self,
            tmp_path: Path,
    ) -> None:
        csv_file = tmp_path / "invalid.csv"
        self._write_csv(
            csv_file,
            (
                "country,year,gdp_growth,inflation,unemployment,population,continent\n"
                "United States,2023,2.1,3.4,3.7,339,North America\n"
            ),
        )

        reader = CsvEconomicDataReader()
        with pytest.raises(ValueError, match="не содержит колонки"):
            reader.read_files((csv_file,))

    def test_read_files_raises_error_when_gdp_is_invalid(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "invalid_gdp.csv"
        self._write_csv(
            csv_file,
            (
                "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
                "United States,2023,wrong,2.1,3.4,3.7,339,North America\n"
            ),
        )

        reader = CsvEconomicDataReader()
        with pytest.raises(ValueError, match="некорректный gdp"):
            reader.read_files((csv_file,))
