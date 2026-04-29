import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from open_webui_admin.cli import cli


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENWEBUI_URL": "http://test", "OPENWEBUI_TOKEN": "test-token"}):
        yield


@pytest.fixture
def runner():
    return CliRunner()


class TestModels:
    def test_models_list(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": "gpt-4o"}, {"id": "gpt-5"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "list"])
            assert "gpt-4o" in result.output
            assert "gpt-5" in result.output
            assert result.exit_code == 0

    def test_models_list_verbose(self, runner, mock_env):
        mock_models_response = MagicMock()
        mock_models_response.json.return_value = {
            "data": [
                {"id": "gpt-5", "owned_by": "openai", "connection_type": "external", "urlIdx": "1"},
                {"id": "anthropic.claude-opus-4-6", "owned_by": "openai", "connection_type": "external", "urlIdx": "0"}
            ]
        }
        mock_models_response.raise_for_status = MagicMock()

        mock_custom_response = MagicMock()
        mock_custom_response.status_code = 200
        mock_custom_response.json.return_value = {"data": []}

        mock_config_response = MagicMock()
        mock_config_response.status_code = 200
        mock_config_response.json.return_value = {
            "OPENAI_API_BASE_URLS": [
                "http://pipeline:9099",
                "https://api.openai.com/v1"
            ]
        }

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_models_response, mock_custom_response, mock_config_response]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "list", "-v"])
            assert "gpt-5" in result.output
            assert "openai" in result.output
            assert "https://api.openai.com/v1" in result.output
            assert "anthropic" in result.output
            assert result.exit_code == 0

    def test_models_list_verbose_with_custom(self, runner, mock_env):
        mock_models_response = MagicMock()
        mock_models_response.json.return_value = {"data": [{"id": "gpt-5"}]}
        mock_models_response.raise_for_status = MagicMock()

        mock_custom_response = MagicMock()
        mock_custom_response.status_code = 200
        mock_custom_response.json.return_value = {
            "data": [
                {"id": "dada", "owned_by": "user", "connection_type": "external", "preset": True}
            ]
        }

        mock_config_response = MagicMock()
        mock_config_response.status_code = 200
        mock_config_response.json.return_value = {
            "OPENAI_API_BASE_URLS": ["http://pipeline:9099"]
        }

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_models_response, mock_custom_response, mock_config_response]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "list", "-v"])
            assert "gpt-5" in result.output
            assert "dada" in result.output
            assert result.exit_code == 0

    def test_models_custom(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": "dada", "preset": True},
                {"id": "gpt-5", "preset": False}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "custom"])
            assert "dada" in result.output
            assert result.exit_code == 0

    def test_models_custom_empty(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "custom"])
            assert "No custom models" in result.output
            assert result.exit_code == 0

    def test_models_check_invalid(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": "gpt-4o"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "check", "--name", "nonexistent"])
            assert "is NOT valid" in result.output
            assert result.exit_code == 1

    def test_models_list(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": "gpt-4o"}, {"id": "gpt-5"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "list"])
            assert "gpt-4o" in result.output
            assert "gpt-5" in result.output
            assert result.exit_code == 0

    def test_models_config(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"DEFAULT_MODELS": ["gpt-4o"]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "config"])
            assert "DEFAULT_MODELS" in result.output
            assert result.exit_code == 0

    def test_models_verify_success(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"choices": [{"message": {"content": "Hi"}}]}'

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "verify", "--name", "gpt-4o"])
            assert "is working" in result.output
            assert result.exit_code == 0

    def test_models_verify_fail_auth(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'data: {"id": "test", "choices": [{"delta": {"content": "Error: 401 - {\\"error\\":{\\"type\\":\\"authentication_error\\"}}}]}'

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "verify", "--name", "claude-opus"])
            assert "NOT working" in result.output
            assert "authentication_error" in result.output

    def test_models_verify_fail_404(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '{"error": {"message": "Model not found"}}'

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "verify", "--name", "nonexistent"])
            assert "NOT working" in result.output
            assert "Model not found" in result.output

    def test_models_verify_all(self, runner, mock_env):
        mock_list_response = MagicMock()
        mock_list_response.json.return_value = {"data": [{"id": "gpt-4o"}, {"id": "gpt-5"}]}
        mock_list_response.raise_for_status = MagicMock()

        mock_custom_response = MagicMock()
        mock_custom_response.status_code = 200
        mock_custom_response.json.return_value = {"data": []}

        mock_verify_response = MagicMock()
        mock_verify_response.status_code = 200
        mock_verify_response.text = '{"choices": [{"message": {"content": "Hi"}}]}'

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_list_response, mock_custom_response]
            mock_client.post.return_value = mock_verify_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "verify", "--all"])
            assert "Verifying" in result.output
            assert "[OK]" in result.output
            assert result.exit_code == 0

    def test_models_verify_all_with_failures(self, runner, mock_env):
        mock_list_response = MagicMock()
        mock_list_response.json.return_value = {"data": [{"id": "gpt-5"}]}
        mock_list_response.raise_for_status = MagicMock()

        mock_custom_response = MagicMock()
        mock_custom_response.status_code = 200
        mock_custom_response.json.return_value = {"data": []}

        mock_verify_response = MagicMock()
        mock_verify_response.status_code = 404
        mock_verify_response.text = '{"error": {"message": "Not found"}}'

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_list_response, mock_custom_response]
            mock_client.post.return_value = mock_verify_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "verify", "--all"])
            assert "Verifying" in result.output
            assert "[FAIL]" in result.output
            assert result.exit_code == 0


class TestConfig:
    def test_config_get(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"OPENAI_API_BASE_URLS": ["http://test"], "OPENAI_API_KEYS": ["key"]}
        mock_response.raise_for_status = MagicMock()

        mock_ollama_response = MagicMock()
        mock_ollama_response.status_code = 200
        mock_ollama_response.json.return_value = {"OLLAMA_BASE_URLS": []}

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_response, mock_ollama_response]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["config", "get"])
            assert "OpenAI" in result.output
            assert result.exit_code == 0

    def test_config_get_json(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"OPENAI_API_BASE_URLS": ["http://test"]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["config", "get", "--json"])
            assert "OPENAI_API_BASE_URLS" in result.output
            assert result.exit_code == 0


class TestConnections:
    def test_connections_verify(self, runner, mock_env):
        mock_openai_config = MagicMock()
        mock_openai_config.json.return_value = {"OPENAI_API_BASE_URLS": ["http://test"], "OPENAI_API_KEYS": ["key"]}
        mock_openai_config.raise_for_status = MagicMock()

        mock_ollama_config = MagicMock()
        mock_ollama_config.json.return_value = {"ENABLE_OLLAMA_API": False, "OLLAMA_BASE_URLS": []}
        mock_ollama_config.raise_for_status = MagicMock()

        mock_verify = MagicMock()
        mock_verify.status_code = 200

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_config, mock_ollama_config]
            mock_client.post.return_value = mock_verify
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["connections", "verify"])
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

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_config, mock_ollama_config]
            mock_client.post.return_value = mock_verify_fail
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["connections", "verify"])
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

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_config, mock_ollama_config]
            mock_client.post.return_value = mock_verify
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["connections", "verify"])
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

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_openai_config, mock_ollama_config]
            mock_client.post.return_value = mock_verify
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["connections", "verify"])
            assert "http://test" in result.output
            assert result.exit_code == 0


class TestBanners:
    def test_banners_get_empty(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["banners", "get"])
            assert "No banners" in result.output
            assert result.exit_code == 0

    def test_banners_get_with_data(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"type": "Info", "title": "Test", "content": "Test content"}]
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["banners", "get"])
            assert "Info" in result.output
            assert "Test" in result.output
            assert result.exit_code == 0

    def test_banners_clear(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["banners", "clear"])
            assert "deleted" in result.output
            assert result.exit_code == 0

    def test_banners_set(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["banners", "set", "--type", "Warning", "--title", "Test", "--content", "Test content"])
            assert result.exit_code == 0


class TestVersion:
    def test_version(self, runner, mock_env):
        result = runner.invoke(cli, ["--version"])
        assert "0.1.0" in result.output


class TestImages:
    def test_images_list(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = ["dall-e-2", "dall-e-3"]
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["images", "list"])
            assert "dall-e-2" in result.output
            assert result.exit_code == 0


class TestAudio:
    def test_audio_models(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"models": [{"id": "tts-1"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["audio", "models"])
            assert "tts-1" in result.output
            assert result.exit_code == 0

    def test_audio_voices(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"voices": [{"id": "alloy"}, {"id": "echo"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["audio", "voices"])
            assert "alloy" in result.output
            assert result.exit_code == 0

    def test_audio_models_list_response(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": "tts-1-hd"}]
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["audio", "models"])
            assert "tts-1-hd" in result.output
            assert result.exit_code == 0


class TestErrors:
    def test_http_error(self, runner, mock_env):
        import httpx

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            message="Error",
            request=MagicMock(),
            response=MagicMock()
        )

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "list"])
            assert result.exit_code != 0

    def test_connection_error(self, runner, mock_env):
        import httpx

        with patch("open_webui_admin.cli.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = httpx.ConnectError("Connection failed")
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "list"])
            assert result.exit_code != 0