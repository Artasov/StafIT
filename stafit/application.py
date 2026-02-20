import sys
from typing import Sequence

from stafit.arguments import CliArgumentParser
from stafit.readers import CsvEconomicDataReader
from stafit.rendering import ConsoleTableRenderer
from stafit.reports import ReportRegistry


class Application:
    """Точка входа CLI-сценария."""

    def __init__(self) -> None:
        self.registry = ReportRegistry.with_default_reports()
        self.reader = CsvEconomicDataReader()
        self.renderer = ConsoleTableRenderer()

    def run(self, argv: Sequence[str] | None = None) -> int:
        """Запускает сценарий и возвращает код завершения."""
        parser = CliArgumentParser(self.registry.available_names())
        try:
            cli_args = parser.parse(argv)
            records = self.reader.read_files(cli_args.files)
            report = self.registry.get(cli_args.report)
            table = report.build(records)
            self.renderer.render(table, sys.stdout)
            return 0
        except SystemExit as error:
            return int(error.code)
        except (OSError, ValueError) as error:
            sys.stderr.write(f"Ошибка: {error}\n")
            return 1
