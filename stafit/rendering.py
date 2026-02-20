from typing import TextIO

from stafit.domain import ReportTable


class ConsoleTableRenderer:
    """Рендерит ReportTable в таблицу."""

    def render(self, table: ReportTable, output: TextIO) -> None:
        text = self._build_table(table)
        output.write(text)
        output.write("\n")

    @staticmethod
    def _build_table(table: ReportTable) -> str:
        widths = ConsoleTableRenderer._calculate_widths(table)
        border = ConsoleTableRenderer._build_border(widths)

        lines = [border, ConsoleTableRenderer._build_row(table.headers, widths), border]
        for row in table.rows:
            lines.append(ConsoleTableRenderer._build_row(row, widths))
        lines.append(border)

        return "\n".join(lines)

    @staticmethod
    def _calculate_widths(table: ReportTable) -> tuple[int, ...]:
        widths = [len(column) for column in table.headers]
        for row in table.rows:
            for index, value in enumerate(row):
                widths[index] = max(widths[index], len(value))
        return tuple(widths)

    @staticmethod
    def _build_border(widths: tuple[int, ...]) -> str:
        parts = ["-" * (width + 2) for width in widths]
        return f"+{'+'.join(parts)}+"

    @staticmethod
    def _build_row(values: tuple[str, ...], widths: tuple[int, ...]) -> str:
        padded = [f" {value.ljust(widths[index])} " for index, value in enumerate(values)]
        return f"|{'|'.join(padded)}|"
