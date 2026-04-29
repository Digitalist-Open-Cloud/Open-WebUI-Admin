import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from open_webui_admin.models import models


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENWEBUI_URL": "http://test", "OPENWEBUI_TOKEN": "test-token"}):
        yield


@pytest.fixture
def runner():
    return CliRunner()


class TestModelsList:
    def test_models_list(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": "gpt-4o"}, {"id": "gpt-5"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["list"])
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

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_models_response, mock_custom_response, mock_config_response]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["list", "-v"])
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

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_models_response, mock_custom_response, mock_config_response]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["list", "-v"])
            assert "gpt-5" in result.output
            assert "dada" in result.output
            assert result.exit_code == 0


class TestModelsCustom:
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

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom"])
            assert "dada" in result.output
            assert result.exit_code == 0

    def test_models_custom_empty(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom"])
            assert "No custom models" in result.output
            assert result.exit_code == 0


class TestModelsCheck:
    def test_models_check_invalid(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": "gpt-4o"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["check", "--name", "nonexistent"])
            assert "is NOT valid" in result.output
            assert result.exit_code == 1


class TestModelsConfig:
    def test_models_config(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"DEFAULT_MODELS": ["gpt-4o"]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["config"])
            assert "DEFAULT_MODELS" in result.output
            assert result.exit_code == 0


class TestModelsVerify:
    def test_models_verify_success(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"choices": [{"message": {"content": "Hi"}}]}'

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["verify", "--name", "gpt-4o"])
            assert "is working" in result.output
            assert result.exit_code == 0

    def test_models_verify_fail_auth(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'data: {"id": "test", "choices": [{"delta": {"content": "Error: 401 - {\\"error\\":{\\"type\\":\\"authentication_error\\"}}}]}'

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["verify", "--name", "claude-opus"])
            assert "NOT working" in result.output
            assert "authentication_error" in result.output

    def test_models_verify_fail_404(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = '{"error": {"message": "Model not found"}}'

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["verify", "--name", "nonexistent"])
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

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_list_response, mock_custom_response]
            mock_client.post.return_value = mock_verify_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["verify", "--all"])
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

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [mock_list_response, mock_custom_response]
            mock_client.post.return_value = mock_verify_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["verify", "--all"])
            assert "Verifying" in result.output
            assert "[FAIL]" in result.output
            assert result.exit_code == 0
