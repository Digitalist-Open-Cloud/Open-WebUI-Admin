import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from open_webui_admin.config import config


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENWEBUI_URL": "http://test", "OPENWEBUI_TOKEN": "test-token"}):
        yield


@pytest.fixture
def runner():
    return CliRunner()


class TestConfigGet:
    def test_config_get_openai(self, runner, mock_env):
        """Test config get --name openai shows OpenAI connections."""
        mock_openai_response = MagicMock()
        mock_openai_response.json.return_value = {"OPENAI_API_BASE_URLS": ["http://test"], "OPENAI_API_KEYS": ["key"]}
        mock_openai_response.raise_for_status = MagicMock()

        mock_ollama_response = MagicMock()
        mock_ollama_response.status_code = 200
        mock_ollama_response.json.return_value = {"OLLAMA_BASE_URLS": []}

        with patch("open_webui_admin.config.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_response, mock_ollama_response]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(config, ["get", "--name", "openai"])
            assert "OpenAI" in result.output
            assert result.exit_code == 0

    def test_config_get_openai_json(self, runner, mock_env):
        """Test config get --name openai --json outputs JSON."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"OPENAI_API_BASE_URLS": ["http://test"]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.config.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(config, ["get", "--name", "openai", "--json"])
            assert "OPENAI_API_BASE_URLS" in result.output
            assert result.exit_code == 0

    def test_config_get_ollama(self, runner, mock_env):
        """Test config get --name ollama shows Ollama config."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"ENABLE_OLLAMA_API": True, "OLLAMA_BASE_URLS": ["http://ollama:11434"]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.config.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(config, ["get", "--name", "ollama"])
            assert "ENABLE_OLLAMA_API" in result.output
            assert result.exit_code == 0

    def test_config_get_ollama_json(self, runner, mock_env):
        """Test config get --name ollama --json outputs JSON."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"ENABLE_OLLAMA_API": True}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.config.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(config, ["get", "--name", "ollama", "--json"])
            assert "ENABLE_OLLAMA_API" in result.output
            assert result.exit_code == 0


class TestConfigExport:
    def test_config_export(self, runner, mock_env):
        """Test config export fetches from /api/v1/configs/export."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"general": {"default_models": ["gpt-4o"]}, "audio": {}}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.config.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(config, ["export"])
            assert "default_models" in result.output
            assert result.exit_code == 0
