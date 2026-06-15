import json
import uuid
import pytest
from unittest.mock import patch, MagicMock

from click.testing import CliRunner


class TestTikaTest:
    """Tests for the tika test command."""

    @pytest.fixture
    def mock_client(self):
        with patch("open_webui_admin.tika.get_client") as mock:
            client = MagicMock()
            mock.return_value.__enter__ = MagicMock(return_value=client)
            mock.return_value.__exit__ = MagicMock(return_value=False)
            yield client

    def test_tika_test_success(self, mock_client, tmp_path):
        # Create a test PDF-like file
        test_pdf = tmp_path / "tika-test.pdf"
        test_pdf.write_bytes(b"%PDF-1.4 fake pdf content for testing.")

        # Upload succeeds
        upload_resp = MagicMock()
        upload_resp.status_code = 200
        upload_resp.json.return_value = {"id": "test-file-123"}
        mock_client.post.return_value = upload_resp

        # Processing status -> success
        status_resp = MagicMock()
        status_resp.status_code = 200
        status_resp.json.return_value = {"status": "success"}
        status_resp.raise_for_status = MagicMock()
        mock_client.get.side_effect = [status_resp]

        # Content
        content_resp = MagicMock()
        content_resp.status_code = 200
        content_resp.text = "Some extracted text from the PDF document that confirms Tika is working."
        # After first get call for status, subsequent gets return content
        side_effects = [status_resp, content_resp]
        mock_client.get.side_effect = side_effects

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", str(test_pdf)])

        assert result.exit_code == 0
        assert "Tika test: PASSED" in result.output
        assert "Uploaded" in result.output or "uploaded" in result.output.lower()

    def test_tika_test_success_json(self, mock_client, tmp_path):
        test_pdf = tmp_path / "tika-test.pdf"
        test_pdf.write_bytes(b"%PDF-1.4")

        upload_resp = MagicMock()
        upload_resp.status_code = 200
        upload_resp.json.return_value = {"id": "file-abc"}
        mock_client.post.return_value = upload_resp

        status_resp = MagicMock()
        status_resp.status_code = 200
        status_resp.json.return_value = {"status": "success"}

        content_resp = MagicMock()
        content_resp.status_code = 200
        content_resp.text = "Extracted PDF content for Tika verification."

        mock_client.get.side_effect = [status_resp, content_resp]

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", str(test_pdf), "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["result"] == "success"
        assert data["file_id"] == "file-abc"
        assert "upload" in data["steps"]
        assert "processing" in data["steps"]

    def test_tika_test_no_default_file(self, mock_client, monkeypatch):
        from unittest.mock import patch
        import os

        # Pretend the default path doesn't exist
        monkeypatch.setattr(os.path, "exists", lambda path: False)

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test"])
        assert result.exit_code == 0
        assert "No file provided" in result.output

    def test_tika_test_file_not_found(self, mock_client):
        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", "/nonexistent/file.pdf"])
        assert result.exit_code == 0
        assert "File not found" in result.output

    def test_tika_test_upload_fails(self, mock_client, tmp_path):
        test_pdf = tmp_path / "tika-test.pdf"
        test_pdf.write_bytes(b"%PDF-1.4")

        upload_resp = MagicMock()
        upload_resp.status_code = 500
        upload_resp.raise_for_status.side_effect = Exception("upload failed")
        mock_client.post.return_value = upload_resp

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", str(test_pdf)])

        assert result.exit_code == 0
        assert "Tika test: FAILED" in result.output
        assert "upload" in result.output.lower()

    def test_tika_test_no_default_file_json(self, mock_client, monkeypatch):
        import os
        monkeypatch.setattr(os.path, "exists", lambda path: False)

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["result"] == "error"

    def test_tika_test_file_not_found_json(self, mock_client):
        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", "/nonexistent/file.pdf", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["result"] == "error"

    def test_tika_test_processing_fails(self, mock_client, tmp_path):
        test_pdf = tmp_path / "tika-test.pdf"
        test_pdf.write_bytes(b"%PDF-1.4")

        upload_resp = MagicMock()
        upload_resp.status_code = 200
        upload_resp.json.return_value = {"id": "f1"}
        mock_client.post.return_value = upload_resp

        status_resp = MagicMock()
        status_resp.status_code = 200
        status_resp.json.return_value = {"status": "processing failed"}
        mock_client.get.return_value = status_resp

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", str(test_pdf)])

        assert result.exit_code == 0
        assert "Tika test: FAILED" in result.output

    def test_tika_test_processing_exception(self, mock_client, tmp_path):
        test_pdf = tmp_path / "tika-test.pdf"
        test_pdf.write_bytes(b"%PDF-1.4")

        upload_resp = MagicMock()
        upload_resp.status_code = 200
        upload_resp.json.return_value = {"id": "f1"}
        mock_client.post.return_value = upload_resp

        status_resp = MagicMock()
        status_resp.status_code = 200
        status_resp.json.side_effect = Exception("status check failed")
        mock_client.get.return_value = status_resp

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", str(test_pdf)])

        assert result.exit_code == 0
        assert "Tika test: FAILED" in result.output

    def test_tika_test_content_retrieval_fails(self, mock_client, tmp_path):
        test_pdf = tmp_path / "tika-test.pdf"
        test_pdf.write_bytes(b"%PDF-1.4")

        upload_resp = MagicMock()
        upload_resp.status_code = 200
        upload_resp.json.return_value = {"id": "f1"}
        mock_client.post.return_value = upload_resp

        status_resp = MagicMock()
        status_resp.status_code = 200
        status_resp.json.return_value = {"status": "success"}
        status_resp.raise_for_status = MagicMock()

        content_resp = MagicMock()
        content_resp.status_code = 500
        content_resp.raise_for_status.side_effect = Exception("content retrieval failed")

        mock_client.get.side_effect = [status_resp, content_resp]

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", str(test_pdf)])

        assert result.exit_code == 0
        assert "Tika test: FAILED" in result.output

    def test_tika_test_short_content(self, mock_client, tmp_path):
        test_pdf = tmp_path / "tika-test.pdf"
        test_pdf.write_bytes(b"%PDF-1.4")

        upload_resp = MagicMock()
        upload_resp.status_code = 200
        upload_resp.json.return_value = {"id": "f1"}
        mock_client.post.return_value = upload_resp

        status_resp = MagicMock()
        status_resp.status_code = 200
        status_resp.json.return_value = {"status": "success"}
        status_resp.raise_for_status = MagicMock()

        content_resp = MagicMock()
        content_resp.status_code = 200
        content_resp.text = "short"
        mock_client.get.side_effect = [status_resp, content_resp]

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", str(test_pdf)])

        assert result.exit_code == 0
        assert "Tika test: FAILED" in result.output
        assert "too short" in result.output

    def test_tika_test_upload_fails_json(self, mock_client, tmp_path):
        test_pdf = tmp_path / "tika-test.pdf"
        test_pdf.write_bytes(b"%PDF-1.4")

        upload_resp = MagicMock()
        upload_resp.status_code = 500
        upload_resp.raise_for_status.side_effect = Exception("upload failed")
        mock_client.post.return_value = upload_resp

        from open_webui_admin.tika import tika
        runner = CliRunner()
        result = runner.invoke(tika, ["test", "--path", str(test_pdf), "--json"])

        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["result"] == "fail"
        assert "upload" in data["steps"]
