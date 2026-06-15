import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from open_webui_admin.audio import audio


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENWEBUI_URL": "http://test", "OPENWEBUI_TOKEN": "test-token"}):
        yield


@pytest.fixture
def runner():
    return CliRunner()


class TestAudioModels:
    def test_audio_models(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"models": [{"id": "tts-1"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["models"])
            assert "tts-1" in result.output
            assert result.exit_code == 0

    def test_audio_models_list_response(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": "tts-1-hd"}]
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["models"])
            assert "tts-1-hd" in result.output
            assert result.exit_code == 0


    def test_audio_models_empty_json(self, runner, mock_env):
        """Empty models with JSON output -> []."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"models": []}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["models", "--json"])
            assert "[]" in result.output
            assert result.exit_code == 0

    def test_audio_models_empty_text(self, runner, mock_env):
        """Empty models with text output -> (none)."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"models": []}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["models"])
            assert "(none)" in result.output
            assert result.exit_code == 0

    def test_audio_models_scalar_fallback(self, runner, mock_env):
        """When data is not dict/list, wrap as single-element list."""
        mock_response = MagicMock()
        mock_response.json.return_value = "single-model-id"
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["models"])
            assert "single-model-id" in result.output
            assert result.exit_code == 0

    def test_audio_models_list_of_strings(self, runner, mock_env):
        """When data is a list of strings, each string is displayed."""
        mock_response = MagicMock()
        mock_response.json.return_value = ["tts-1", "tts-1-hd"]
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["models"])
            assert "tts-1" in result.output
            assert "tts-1-hd" in result.output
            assert result.exit_code == 0


class TestAudioVoices:
    def test_audio_voices(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = {"voices": [{"id": "alloy"}, {"id": "echo"}]}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["voices"])
            assert "alloy" in result.output
            assert result.exit_code == 0

    def test_audio_voices_empty_json(self, runner, mock_env):
        """Empty voices with JSON output -> []."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"voices": []}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["voices", "--json"])
            assert "[]" in result.output
            assert result.exit_code == 0

    def test_audio_voices_empty_text(self, runner, mock_env):
        """Empty voices with text output -> (none)."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"voices": []}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["voices"])
            assert "(none)" in result.output
            assert result.exit_code == 0

    def test_audio_voices_scalar_fallback(self, runner, mock_env):
        """When voices data is not dict/list, wrap as single-element list."""
        mock_response = MagicMock()
        mock_response.json.return_value = "single-voice-id"
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["voices"])
            assert "single-voice-id" in result.output
            assert result.exit_code == 0

    def test_audio_voices_list_of_strings(self, runner, mock_env):
        """When voices data is a list of strings, each string is displayed."""
        mock_response = MagicMock()
        mock_response.json.return_value = ["alloy", "echo", "fable"]
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.audio.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(audio, ["voices"])
            assert "alloy" in result.output
            assert "echo" in result.output
            assert result.exit_code == 0
