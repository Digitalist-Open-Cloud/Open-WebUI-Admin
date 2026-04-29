import json
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from open_webui_admin.files import files


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_client():
    with patch("open_webui_admin.files.get_client") as mock:
        mock_client = MagicMock()
        mock.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock.return_value.__exit__ = MagicMock(return_value=False)
        yield mock_client


class TestFilesList:
    def test_files_list_empty(self, runner, mock_client):
        mock_client.get.return_value.json.return_value = []
        result = runner.invoke(files, ["list"])
        assert result.exit_code == 0
        assert "No files" in result.output

    def test_files_list(self, runner, mock_client):
        mock_client.get.return_value.json.return_value = [
            {"id": "file1", "meta": {"name": "test.pdf", "size": 1024}},
            {"id": "file2", "meta": {"name": "doc.txt", "size": 2048}},
        ]
        result = runner.invoke(files, ["list"])
        assert result.exit_code == 0
        assert "file1" in result.output
        assert "test.pdf" in result.output


class TestFilesShow:
    def test_files_show_not_found(self, runner, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_client.get.return_value = mock_response
        result = runner.invoke(files, ["show", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_files_show(self, runner, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "file1", "meta": {"name": "test.pdf", "size": 1024, "content_type": "application/pdf"}
        }
        mock_client.get.return_value = mock_response
        result = runner.invoke(files, ["show", "file1"])
        assert result.exit_code == 0
        assert "test.pdf" in result.output
        assert "1024 bytes" in result.output


class TestFilesUpload:
    def test_files_upload(self, runner, mock_client, tmp_path):
        import mimetypes
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello")
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "new-file-id"}
        mock_client.post.return_value = mock_response
        result = runner.invoke(files, ["upload", str(test_file)])
        assert result.exit_code == 0
        assert "Uploaded" in result.output
        assert "new-file-id" in result.output


class TestFilesDelete:
    def test_files_delete(self, runner, mock_client):
        mock_response = MagicMock()
        mock_client.delete.return_value = mock_response
        result = runner.invoke(files, ["delete", "file1"])
        assert result.exit_code == 0
        assert "Deleted: file1" in result.output
