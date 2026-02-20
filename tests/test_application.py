from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from stafit.application import Application


class TestApplication:
    @staticmethod
    def _write_csv(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8", newline="")

    def test_run_builds_average_gdp_report(self, tmp_path: Path) -> None:
        first_file = tmp_path / "economy_1.csv"
        second_file = tmp_path / "economy_2.csv"
        self._write_csv(
            first_file,
            (
                "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
                "United States,2023,25462,2.1,3.4,3.7,339,North America\n"
                "China,2023,17963,5.2,2.5,5.2,1425,Asia\n"
            ),
        )
        self._write_csv(
            second_file,
            (
                "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
                "United States,2022,23315,2.1,8.0,3.6,338,North America\n"
                "China,2022,17734,3.0,2.0,5.6,1423,Asia\n"
                "Germany,2023,4086,-0.3,6.2,3.0,83,Europe\n"
            ),
        )

        output = StringIO()
        error_output = StringIO()
        app = Application()

        with redirect_stdout(output), redirect_stderr(error_output):
            code = app.run(
                (
                    "--files",
                    str(first_file),
                    str(second_file),
                    "--report",
                    "average-gdp",
                )
            )

        assert code == 0
        rendered = output.getvalue()
        assert "United States" in rendered
        assert "24388.50" in rendered
        assert "China" in rendered
        assert "17848.50" in rendered
        assert "Germany" in rendered
        assert "4086.00" in rendered
        assert rendered.index("United States") < rendered.index("China")
        assert rendered.index("China") < rendered.index("Germany")
        assert error_output.getvalue() == ""

    def test_run_returns_error_when_file_does_not_exist(self, tmp_path: Path) -> None:
        missing_file = tmp_path / "missing.csv"
        output = StringIO()
        error_output = StringIO()
        app = Application()

        with redirect_stdout(output), redirect_stderr(error_output):
            code = app.run(("--files", str(missing_file), "--report", "average-gdp"))

        assert code == 1
        assert output.getvalue() == ""
        assert "Ошибка:" in error_output.getvalue()

    def test_run_returns_argparse_error_for_unknown_report(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "economy.csv"
        self._write_csv(
            csv_file,
            (
                "country,year,gdp,gdp_growth,inflation,unemployment,population,continent\n"
                "United States,2023,25462,2.1,3.4,3.7,339,North America\n"
            ),
        )
        output = StringIO()
        error_output = StringIO()
        app = Application()

        with redirect_stdout(output), redirect_stderr(error_output):
            code = app.run(("--files", str(csv_file), "--report", "unknown-report"))

        assert code == 2
