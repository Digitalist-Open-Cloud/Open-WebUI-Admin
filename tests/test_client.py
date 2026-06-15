import click
import pytest
from unittest.mock import patch, MagicMock
import httpx


class TestGetClient:
    def test_get_client_missing_url(self):
        """get_client raises ClickException when URL is missing."""
        from open_webui_admin.client import get_client

        with patch("open_webui_admin.client.OPENWEBUI_URL", ""):
            with patch("open_webui_admin.client.TOKEN", "token"):
                with pytest.raises(click.ClickException, match="OPENWEBUI_URL"):
                    get_client()

    def test_get_client_missing_token(self):
        """get_client raises ClickException when TOKEN is missing."""
        from open_webui_admin.client import get_client

        with patch("open_webui_admin.client.OPENWEBUI_URL", "http://test"):
            with patch("open_webui_admin.client.TOKEN", ""):
                with pytest.raises(click.ClickException, match="TOKEN"):
                    get_client()

    def test_get_client_success(self):
        """get_client returns an httpx.Client with correct config."""
        from open_webui_admin.client import get_client

        with patch("open_webui_admin.client.OPENWEBUI_URL", "http://test"):
            with patch("open_webui_admin.client.TOKEN", "test-token"):
                client = get_client()
                assert isinstance(client, httpx.Client)
                assert client.base_url == "http://test"
                assert client.headers["Authorization"] == "Bearer test-token"
                client.close()
