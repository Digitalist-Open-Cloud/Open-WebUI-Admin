import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from open_webui_admin.banners import banners


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENWEBUI_URL": "http://test", "OPENWEBUI_TOKEN": "test-token"}):
        yield


@pytest.fixture
def runner():
    return CliRunner()


class TestBannersGet:
    def test_banners_get_empty(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.banners.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(banners, ["get"])
            assert "No banners" in result.output
            assert result.exit_code == 0

    def test_banners_get_with_data(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"type": "Info", "title": "Test", "content": "Test content"}]
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.banners.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(banners, ["get"])
            assert "Info" in result.output
            assert "Test" in result.output
            assert result.exit_code == 0


class TestBannersClear:
    def test_banners_clear(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.banners.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(banners, ["clear"])
            assert "deleted" in result.output
            assert result.exit_code == 0


class TestBannersSet:
    def test_banners_set(self, runner, mock_env):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.banners.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(banners, ["set", "--type", "Warning", "--title", "Test", "--content", "Test content"])
            assert result.exit_code == 0
