import pytest
from unittest.mock import patch, MagicMock
import json
import sys

from open_webui_admin.output import print_table, print_kv, print_json, print_success, print_error, print_warning, die


class TestPrintTable:
    def test_print_table_json_output(self, capsys):
        """JSON output when rows is empty."""
        print_table([], [("ID", "id", 20)], json_output=True)
        captured = capsys.readouterr()
        assert "[]" in captured.out

    def test_print_table_empty_rows_no_json(self, capsys):
        """Empty rows with no JSON output -> (none)."""
        print_table([], [("ID", "id", 20)])
        captured = capsys.readouterr()
        assert "(none)" in captured.out

    def test_print_table_simple_output(self, capsys):
        """Simple output: values concatenated."""
        rows = [{"id": "gpt-4o", "name": "GPT-4"}]
        cols = [("ID", "id", 10), ("NAME", "name", 10)]
        print_table(rows, cols, simple_output=True)
        captured = capsys.readouterr()
        assert "gpt-4o" in captured.out
        assert "GPT-4" in captured.out


class TestPrintKv:
    def test_print_kv_json(self, capsys):
        """JSON output for key-value pairs."""
        print_kv([("key1", "val1")], json_output=True)
        captured = capsys.readouterr()
        assert '"key1": "val1"' in captured.out

    def test_print_kv_simple(self, capsys):
        """Simple output for key-value pairs."""
        print_kv([("key1", "val1"), ("key2", "val2")], simple_output=True)
        captured = capsys.readouterr()
        assert "val1" in captured.out
        assert "val2" in captured.out

    def test_print_kv_empty(self, capsys):
        """Empty pairs should produce no output."""
        print_kv([])
        captured = capsys.readouterr()
        assert captured.out == ""


class TestWarnings:
    def test_print_warning(self, capsys):
        """print_warning outputs yellow warning message."""
        print_warning("test warning")
        captured = capsys.readouterr()
        assert "test warning" in captured.out

    def test_die(self):
        """die prints error and exits with code."""
        with pytest.raises(SystemExit) as exc_info:
            die("fatal error")
        assert exc_info.value.code == 1
