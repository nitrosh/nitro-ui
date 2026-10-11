import csv
import json
import warnings

from nitro_ui.core.element import HTMLElement, register_tag
from nitro_ui.tags.tag_factory import simple_tag_class

TableFooter = simple_tag_class("tfoot")
TableHeaderCell = simple_tag_class("th")
TableHeader = simple_tag_class("thead")
TableBody = simple_tag_class("tbody")
TableDataCell = simple_tag_class("td")
TableRow = simple_tag_class("tr")
Caption = simple_tag_class("caption")
Col = simple_tag_class("col", self_closing=True)
Colgroup = simple_tag_class("colgroup")


class Table(HTMLElement):
    """HTML ``<table>`` element with helpers for loading data from files."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{**kwargs, "tag": "table"})

    @classmethod
    def from_csv(cls, file_path: str, encoding: str = "utf-8") -> "Table":
        """Load a CSV file into a ``<table>`` of ``<tr>`` / ``<td>`` rows.

        Every row becomes a ``TableRow``; every cell becomes a
        ``TableDataCell``. The first row is not treated specially - wrap
        it in a ``TableHeader`` yourself if you need ``<th>``.

        Args:
            file_path: Path to a CSV file on disk.
            encoding: Text encoding to read the file as.

        Returns:
            A populated ``Table`` instance.

        Raises:
            ValueError: If the file is missing, has an encoding mismatch,
                or cannot be parsed as CSV.

        Example:
            >>> Table.from_csv("data.csv").render()  # doctest: +SKIP
        """
        table = cls()
        try:
            with open(file_path, mode="r", encoding=encoding) as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    table_row = TableRow()
                    for cell in row:
                        table_row.append(TableDataCell(cell))
                    table.append(table_row)
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except csv.Error as e:
            raise ValueError(f"CSV error occurred: {e}")
        except UnicodeDecodeError:
            raise ValueError(f"Encoding error: {encoding} is not suitable for the file")
        return table

    @classmethod
    def from_json(
        cls, json_str: str, encoding: str = "utf-8", allow_partial_files: bool = False
    ) -> "Table":
        """Reconstruct a table from a ``to_json()`` result.

        Behaves like ``HTMLElement.from_json()``. Passing a file path still
        works for backward compatibility but is deprecated; use
        ``from_json_file()`` for that.

        Args:
            json_str: JSON previously produced by ``to_json()``.
            encoding: Only used by the deprecated file-path form.
            allow_partial_files: See ``HTMLElement.from_dict()``.
        """
        if json_str.lstrip().startswith("{"):
            return super().from_json(json_str, allow_partial_files=allow_partial_files)
        warnings.warn(
            "Table.from_json(path) is deprecated; use Table.from_json_file(path).",
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.from_json_file(json_str, encoding=encoding)

    @classmethod
    def from_json_file(cls, file_path: str, encoding: str = "utf-8") -> "Table":
        """Load a JSON file (a list of row-lists) into a ``<table>``.

        The file must decode to a list of lists; each inner list is
        rendered as a row of ``<td>`` cells (values are stringified).

        Args:
            file_path: Path to a JSON file on disk.
            encoding: Text encoding to read the file as.

        Returns:
            A populated ``Table`` instance.

        Raises:
            ValueError: If the file is missing, has an encoding mismatch,
                is not valid JSON, or is not a list-of-lists.
        """
        table = cls()
        try:
            with open(file_path, mode="r", encoding=encoding) as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("JSON data must be a list of rows")
                for row in data:
                    if not isinstance(row, list):
                        raise ValueError("Each row in JSON data must be a list")
                    table_row = TableRow()
                    for cell in row:
                        table_row.append(TableDataCell(str(cell)))
                    table.append(table_row)
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON decoding error: {e}")
        except UnicodeDecodeError:
            raise ValueError(f"Encoding error: {encoding} is not suitable for the file")
        return table


register_tag("table", Table)
