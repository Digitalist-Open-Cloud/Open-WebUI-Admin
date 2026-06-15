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
    def test_custom_list(self, runner, mock_env):
        """Test models custom list."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "dada", "base_model_id": "gpt-4o"},
                {"id": "test-model", "base_model_id": "claude-3"}
            ],
            "total": 2
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "list"])
            assert result.exit_code == 0
            assert "dada" in result.output
            assert "gpt-4o" in result.output

    def test_custom_list_with_name(self, runner, mock_env):
        """Test models custom list --name shows full JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "dada", "base_model_id": "gpt-4o", "name": "Dada", "params": {"system": "You are dada"}}
            ],
            "total": 1
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "list"])
            assert result.exit_code == 0
            assert "dada" in result.output
            assert "gpt-4o" in result.output

    def test_custom_list_with_name(self, runner, mock_env):
        """Test models custom list --name shows full JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"id": "dada", "base_model_id": "gpt-4o", "name": "Dada", "params": {"system": "You are dada"}}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "list", "--name", "dada"])
            assert '"base_model_id": "gpt-4o"' in result.output
            assert '"name": "Dada"' in result.output
            assert result.exit_code == 0

    def test_custom_list_with_name_not_found(self, runner, mock_env):
        """Test models custom list --name with non-existent model."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [], "total": 0}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "list", "--name", "nonexistent"])
            assert "not found" in result.output
            assert result.exit_code == 1

    def test_custom_list_empty(self, runner, mock_env):
        """Test models custom list with no custom models."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [], "total": 0}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "list"])
            assert "No custom models" in result.output
            assert result.exit_code == 0

    def test_custom_verify_all(self, runner, mock_env):
        """Test models custom verify --all."""
        mock_list_response = MagicMock()
        mock_list_response.status_code = 200
        mock_list_response.json.return_value = {"items": [{"id": "dada"}, {"id": "test-model"}], "total": 2}
        mock_list_response.raise_for_status = MagicMock()

        mock_verify_response = MagicMock()
        mock_verify_response.status_code = 200
        mock_verify_response.text = '{"choices": [{"message": {"content": "Hi"}}]}'

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_list_response
            mock_client.post.return_value = mock_verify_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "verify", "--all"])
            assert "Verifying" in result.output
            assert "[OK]" in result.output
            assert result.exit_code == 0

    def test_custom_verify_all_retry_max_completion_tokens(self, runner, mock_env):
        """Test retry with max_completion_tokens on max_tokens error."""
        mock_list_response = MagicMock()
        mock_list_response.status_code = 200
        mock_list_response.json.return_value = {"items": [{"id": "chatgpt-53-fast"}], "total": 1}
        mock_list_response.raise_for_status = MagicMock()

        mock_fail_response = MagicMock()
        mock_fail_response.status_code = 400
        mock_fail_response.text = '{"error": {"message": "Unsupported parameter: \'max_tokens\' is not supported with this model. Use \'max_completion_tokens\' instead."}}'

        mock_success_response = MagicMock()
        mock_success_response.status_code = 200
        mock_success_response.text = '{"choices": [{"message": {"content": "Hi"}}]}'

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_list_response
            mock_client.post.side_effect = [mock_fail_response, mock_success_response]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "verify", "--all", "-v"])
            assert "[OK] chatgpt-53-fast" in result.output
            assert result.exit_code == 0

    def test_custom_verify_all_retry_max_completion_tokens_fail(self, runner, mock_env):
        """Test retry with max_completion_tokens still fails."""
        mock_list_response = MagicMock()
        mock_list_response.status_code = 200
        mock_list_response.json.return_value = {"items": [{"id": "chatgpt-53-fast"}], "total": 1}
        mock_list_response.raise_for_status = MagicMock()

        mock_fail_response1 = MagicMock()
        mock_fail_response1.status_code = 400
        mock_fail_response1.text = '{"error": {"message": "Unsupported parameter: \'max_tokens\' is not supported with this model. Use \'max_completion_tokens\' instead."}}'

        mock_fail_response2 = MagicMock()
        mock_fail_response2.status_code = 400
        mock_fail_response2.text = '{"error": {"message": "Model unavailable"}}'

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_list_response
            mock_client.post.side_effect = [mock_fail_response1, mock_fail_response2]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "verify", "--all"])
            assert "[FAIL]" in result.output
            assert "Model unavailable" in result.output
            assert result.exit_code == 0

    def test_custom_verify_all_retry_max_completion_tokens_200_error(self, runner, mock_env):
        """Test retry when max_tokens error comes via 200 response with error body."""
        mock_list_response = MagicMock()
        mock_list_response.status_code = 200
        mock_list_response.json.return_value = {"items": [{"id": "o1-model"}], "total": 1}
        mock_list_response.raise_for_status = MagicMock()

        mock_fail_response = MagicMock()
        mock_fail_response.status_code = 200
        mock_fail_response.text = '{"error": {"message": "Unsupported parameter: \'max_tokens\' is not supported with this model. Use \'max_completion_tokens\' instead."}}'

        mock_success_response = MagicMock()
        mock_success_response.status_code = 200
        mock_success_response.text = '{"choices": [{"message": {"content": "Hi"}}]}'

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_list_response
            mock_client.post.side_effect = [mock_fail_response, mock_success_response]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "verify", "--all"])
            assert "[OK]" in result.output
            assert result.exit_code == 0

    def test_custom_verify_name(self, runner, mock_env):
        """Test models custom verify --name."""
        mock_list_response = MagicMock()
        mock_list_response.status_code = 200
        mock_list_response.json.return_value = {"items": [{"id": "dada"}], "total": 1}
        mock_list_response.raise_for_status = MagicMock()

        mock_verify_response = MagicMock()
        mock_verify_response.status_code = 200
        mock_verify_response.text = '{"choices": [{"message": {"content": "Hi"}}]}'

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_list_response
            mock_client.post.return_value = mock_verify_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(models, ["custom", "verify", "--name", "dada"])
            assert "is working" in result.output
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
