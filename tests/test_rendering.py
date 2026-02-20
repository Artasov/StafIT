from io import StringIO

from stafit.domain import ReportTable
from stafit.rendering import ConsoleTableRenderer


class TestConsoleTableRenderer:
    def test_render_formats_ascii_table(self) -> None:
        table = ReportTable(
            headers=("country", "average_gdp"),
            rows=(("United States", "23923.67"), ("China", "17810.33")),
        )

        output = StringIO()
        renderer = ConsoleTableRenderer()
        renderer.render(table, output)

        expected = (
            "+---------------+-------------+\n"
            "| country       | average_gdp |\n"
            "+---------------+-------------+\n"
            "| United States | 23923.67    |\n"
            "| China         | 17810.33    |\n"
            "+---------------+-------------+\n"
        )
        assert output.getvalue() == expected
