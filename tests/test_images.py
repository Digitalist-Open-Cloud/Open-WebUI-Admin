import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from open_webui_admin.images import images


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENWEBUI_URL": "http://test", "OPENWEBUI_TOKEN": "test-token"}):
        yield


@pytest.fixture
def runner():
    return CliRunner()


class TestImagesList:
    def test_images_list(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = ["dall-e-2", "dall-e-3"]
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.images.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(images, ["list"])
            assert "dall-e-2" in result.output
            assert result.exit_code == 0
