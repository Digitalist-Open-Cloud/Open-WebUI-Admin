import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from open_webui_admin.connections import connections


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENWEBUI_URL": "http://test", "OPENWEBUI_TOKEN": "test-token"}):
        yield


@pytest.fixture
def runner():
    return CliRunner()


class TestConnectionsVerify:
    def test_connections_verify(self, runner, mock_env):
        mock_openai_config = MagicMock()
        mock_openai_config.json.return_value = {"OPENAI_API_BASE_URLS": ["http://test"], "OPENAI_API_KEYS": ["key"]}
        mock_openai_config.raise_for_status = MagicMock()

        mock_ollama_config = MagicMock()
        mock_ollama_config.json.return_value = {"ENABLE_OLLAMA_API": False, "OLLAMA_BASE_URLS": []}
        mock_ollama_config.raise_for_status = MagicMock()

        mock_verify = MagicMock()
        mock_verify.status_code = 200

        with patch("open_webui_admin.connections.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_config, mock_ollama_config]
            mock_client.post.return_value = mock_verify
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(connections, ["verify"])
            assert "OpenAI" in result.output
            assert result.exit_code == 0

    def test_connections_verify_openai_fail(self, runner, mock_env):
        mock_openai_config = MagicMock()
        mock_openai_config.json.return_value = {"OPENAI_API_BASE_URLS": ["http://test"], "OPENAI_API_KEYS": ["key"]}
        mock_openai_config.raise_for_status = MagicMock()

        mock_ollama_config = MagicMock()
        mock_ollama_config.json.return_value = {"ENABLE_OLLAMA_API": False, "OLLAMA_BASE_URLS": []}
        mock_ollama_config.raise_for_status = MagicMock()

        mock_verify_fail = MagicMock()
        mock_verify_fail.status_code = 500

        with patch("open_webui_admin.connections.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_config, mock_ollama_config]
            mock_client.post.return_value = mock_verify_fail
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(connections, ["verify"])
            assert "FAIL" in result.output
            assert result.exit_code == 0

    def test_connections_verify_ollama_enabled_with_urls(self, runner, mock_env):
        mock_openai_config = MagicMock()
        mock_openai_config.json.return_value = {"OPENAI_API_BASE_URLS": [], "OPENAI_API_KEYS": []}
        mock_openai_config.raise_for_status = MagicMock()

        mock_ollama_config = MagicMock()
        mock_ollama_config.json.return_value = {"ENABLE_OLLAMA_API": True, "OLLAMA_BASE_URLS": ["http://ollama:11434"]}
        mock_ollama_config.raise_for_status = MagicMock()

        mock_verify = MagicMock()
        mock_verify.status_code = 200

        with patch("open_webui_admin.connections.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_config, mock_ollama_config]
            mock_client.post.return_value = mock_verify
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(connections, ["verify"])
            assert "ollama" in result.output.lower()
            assert result.exit_code == 0

    def test_connections_verify_no_openai_keys(self, runner, mock_env):
        mock_openai_config = MagicMock()
        mock_openai_config.json.return_value = {"OPENAI_API_BASE_URLS": ["http://test"], "OPENAI_API_KEYS": []}
        mock_openai_config.raise_for_status = MagicMock()

        mock_ollama_config = MagicMock()
        mock_ollama_config.json.return_value = {"ENABLE_OLLAMA_API": False, "OLLAMA_BASE_URLS": []}
        mock_ollama_config.raise_for_status = MagicMock()

        mock_verify = MagicMock()
        mock_verify.status_code = 200

        with patch("open_webui_admin.connections.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_config, mock_ollama_config]
            mock_client.post.return_value = mock_verify
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(connections, ["verify"])
            assert "http://test" in result.output
            assert result.exit_code == 0
