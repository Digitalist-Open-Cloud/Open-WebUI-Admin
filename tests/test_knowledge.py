import json
import os
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

from open_webui_admin.knowledge import knowledge


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_client():
    with patch("open_webui_admin.knowledge.get_client") as mock:
        mock_client = MagicMock()
        mock.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock.return_value.__exit__ = MagicMock(return_value=False)
        yield mock_client


class TestKnowledgeList:
    def test_knowledge_list_empty(self, runner, mock_client):
        mock_client.get.return_value.json.return_value = []
        result = runner.invoke(knowledge, ["list"])
        assert result.exit_code == 0
        assert "No knowledge bases" in result.output

    def test_knowledge_list(self, runner, mock_client):
        mock_client.get.return_value.json.return_value = [
            {"id": "kb1", "name": "Test KB 1"},
            {"id": "kb2", "name": "Test KB 2"},
        ]
        result = runner.invoke(knowledge, ["list"])
        assert result.exit_code == 0
        assert "kb1" in result.output
        assert "kb2" in result.output


class TestKnowledgeShow:
    def test_knowledge_show_not_found(self, runner, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_client.get.return_value = mock_response
        result = runner.invoke(knowledge, ["show", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_knowledge_show(self, runner, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "kb1", "name": "Test KB", "description": "A test knowledge base"
        }
        mock_client.get.return_value = mock_response
        result = runner.invoke(knowledge, ["show", "kb1"])
        assert result.exit_code == 0
        assert "Test KB" in result.output


class TestKnowledgeFiles:
    def test_knowledge_files_not_found(self, runner, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_client.get.return_value = mock_response
        result = runner.invoke(knowledge, ["files", "nonexistent"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_knowledge_files(self, runner, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "file1", "meta": {"name": "test.pdf"}},
                {"id": "file2", "meta": {"name": "doc.txt"}},
            ]
        }
        mock_client.get.return_value = mock_response
        result = runner.invoke(knowledge, ["files", "kb1"])
        assert result.exit_code == 0
        assert "file1" in result.output
        assert "test.pdf" in result.output


class TestKnowledgeCreate:
    def test_knowledge_create(self, runner, mock_client):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "new-kb-id"}
        mock_client.post.return_value = mock_response
        result = runner.invoke(knowledge, ["create", "--name", "New KB", "--description", "Desc"])
        assert result.exit_code == 0
        assert "new-kb-id" in result.output


class TestKnowledgeDelete:
    def test_knowledge_delete(self, runner, mock_client):
        mock_response = MagicMock()
        mock_client.delete.return_value = mock_response
        result = runner.invoke(knowledge, ["delete", "kb1"])
        assert result.exit_code == 0
        assert "Deleted: kb1" in result.output


class TestKnowledgeAddFile:
    def test_knowledge_add_file(self, runner, mock_client):
        mock_response = MagicMock()
        mock_client.post.return_value = mock_response
        result = runner.invoke(knowledge, ["add-file", "kb1", "file1"])
        assert result.exit_code == 0
        assert "Added file1 to kb1" in result.output


class TestKnowledgeRemoveFile:
    def test_knowledge_remove_file(self, runner, mock_client):
        mock_response = MagicMock()
        mock_client.post.return_value = mock_response
        result = runner.invoke(knowledge, ["remove-file", "kb1", "file1"])
        assert result.exit_code == 0
        assert "Removed file1 from kb1" in result.output


class TestKnowledgeAddFolder:
    def test_add_folder_kb_not_found(self, runner, mock_client, tmp_path):
        # First call (KB check) returns 404, subsequent calls work
        mock_response_404 = MagicMock()
        mock_response_404.status_code = 404
        mock_client.get.return_value = mock_response_404
        result = runner.invoke(knowledge, ["add-folder", "nonexistent", str(tmp_path)])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_add_folder_not_a_directory(self, runner, mock_client):
        result = runner.invoke(knowledge, ["add-folder", "kb1", "/nonexistent/path/xyz"])
        assert result.exit_code == 1
        assert "not a valid directory" in result.output

    def test_add_folder_empty(self, runner, mock_client, tmp_path):
        # Create KB mock
        mock_kb_response = MagicMock()
        mock_kb_response.status_code = 200
        mock_kb_response.json.return_value = {"id": "kb1"}
        # Empty folder
        mock_client.get.return_value = mock_kb_response
        result = runner.invoke(knowledge, ["add-folder", "kb1", str(tmp_path)])
        assert result.exit_code == 0
        assert "No files found" in result.output

    def test_add_folder_with_files(self, runner, mock_client, tmp_path):
        # Create test files
        (tmp_path / "test1.pdf").write_text("pdf content")
        (tmp_path / "test2.txt").write_text("text content")

        # Mock KB exists
        mock_kb_response = MagicMock()
        mock_kb_response.status_code = 200
        mock_client.get.return_value = mock_kb_response

        # Mock file upload response
        mock_upload_response = MagicMock()
        mock_upload_response.json.return_value = {"id": "file-001"}
        mock_client.post.return_value = mock_upload_response

        result = runner.invoke(knowledge, ["add-folder", "kb1", str(tmp_path)])
        assert result.exit_code == 0
        assert "Found 2 file(s)" in result.output
        assert "Uploaded" in result.output

    def test_add_folder_pattern(self, runner, mock_client, tmp_path):
        # Create test files
        (tmp_path / "test1.pdf").write_text("pdf content")
        (tmp_path / "test2.txt").write_text("text content")

        # Mock KB exists
        mock_kb_response = MagicMock()
        mock_kb_response.status_code = 200
        mock_client.get.return_value = mock_kb_response

        # Mock file upload response
        mock_upload_response = MagicMock()
        mock_upload_response.json.return_value = {"id": "file-001"}
        mock_client.post.return_value = mock_upload_response

        # Only match PDFs
        result = runner.invoke(knowledge, ["add-folder", "kb1", str(tmp_path), "--pattern", "*.pdf"])
        assert result.exit_code == 0
        assert "Found 1 file(s)" in result.output
