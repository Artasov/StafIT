from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class CliArguments:
    files: tuple[Path, ...]
    report: str


class CliArgumentParser:
    """Парсер аргументов CLI."""

    def __init__(self, available_reports: tuple[str, ...]):
        self.available_reports = available_reports

    def parse(self, argv: Sequence[str] | None = None) -> CliArguments:
        parser = self._build_parser()
        parsed = parser.parse_args(argv)
        files = tuple(Path(path) for path in parsed.files)
        return CliArguments(files=files, report=parsed.report)

    def _build_parser(self) -> ArgumentParser:
        parser = ArgumentParser(
            prog="stafit",
            description="Формирует отчеты по макроэкономическим CSV-файлам.",
        )
        parser.add_argument(
            "--files",
            nargs="+",
            required=True,
            help="Пути до CSV-файлов.",
        )
        parser.add_argument(
            "--report",
            required=True,
            choices=self.available_reports,
            help="Название отчета.",
        )
        return parser
