import pytest
from click.testing import CliRunner
from open_webui_admin.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestVersion:
    def test_version(self, runner):
        result = runner.invoke(cli, ["--version"])
        assert "0.1.0" in result.output


class TestErrors:
    def test_http_error(self, runner):
        import httpx
        from unittest.mock import patch, MagicMock

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            message="Error",
            request=MagicMock(),
            response=MagicMock()
        )

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "list"])
            assert result.exit_code != 0

    def test_connection_error(self, runner):
        import httpx
        from unittest.mock import patch, MagicMock

        with patch("open_webui_admin.models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = httpx.ConnectError("Connection failed")
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(cli, ["models", "list"])
            assert result.exit_code != 0
