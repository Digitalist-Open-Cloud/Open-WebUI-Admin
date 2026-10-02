import json
import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from open_webui_admin.users import users


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"OPENWEBUI_URL": "http://test", "OPENWEBUI_TOKEN": "test-token"}):
        yield


@pytest.fixture
def runner():
    return CliRunner()


class TestUsersGet:
    def test_users_get_all(self, runner, mock_env):
        """Test users get --all lists all users."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": "user-1", "name": "Alice", "email": "alice@test.com", "role": "admin"},
                {"id": "user-2", "name": "Bob", "email": "bob@test.com", "role": "user"}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all"])
            assert "Alice" in result.output
            assert "Bob" in result.output
            assert "Total: 2 users" in result.output
            assert result.exit_code == 0

    def test_users_get_all_json(self, runner, mock_env):
        """Test users get --all --json outputs JSON."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": "user-1", "name": "Alice", "email": "alice@test.com", "role": "admin"}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all", "--json"])
            assert "users" in result.output
            assert result.exit_code == 0

    def test_users_get_all_empty(self, runner, mock_env):
        """Test users get --all with no users."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"users": []}
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all"])
            assert "No users found" in result.output
            assert result.exit_code == 0

    def test_users_get_exclude_email(self, runner, mock_env):
        """Test users get --all --exclude-email filters out matching emails."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": "user-1", "name": "Alice", "email": "alice@digitalist.com", "role": "admin"},
                {"id": "user-2", "name": "Bob", "email": "bob@test.com", "role": "user"},
                {"id": "user-3", "name": "Charlie", "email": "charlie@foo.com", "role": "user"}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all", "--exclude-email", "digitalist"])
            assert "Alice" not in result.output
            assert "Bob" in result.output
            assert "Total: 2 users" in result.output
            assert result.exit_code == 0

    def test_users_get_exclude_email_multiple(self, runner, mock_env):
        """Test users get --all --exclude-email with multiple patterns."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": "user-1", "name": "Alice", "email": "alice@digitalist.com", "role": "admin"},
                {"id": "user-2", "name": "Bob", "email": "bob@test.com", "role": "user"},
                {"id": "user-3", "name": "Charlie", "email": "charlie@foo.com", "role": "user"}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all", "--exclude-email", "digitalist", "--exclude-email", "foo"])
            assert "Alice" not in result.output
            assert "Charlie" not in result.output
            assert "Bob" in result.output
            assert "Total: 1 users" in result.output
            assert result.exit_code == 0

    def test_users_get_include_email(self, runner, mock_env):
        """Test users get --all --include-email filters to matching emails."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": "user-1", "name": "Alice", "email": "alice@digitalist.com", "role": "admin"},
                {"id": "user-2", "name": "Bob", "email": "bob@test.com", "role": "user"},
                {"id": "user-3", "name": "Charlie", "email": "charlie@foo.com", "role": "user"}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all", "--include-email", "digitalist"])
            assert "Alice" in result.output
            assert "Bob" not in result.output
            assert "Charlie" not in result.output
            assert "Total: 1 users" in result.output
            assert result.exit_code == 0

    def test_users_get_include_email_regex(self, runner, mock_env):
        """Test users get --all --include-email with regex pattern."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": "user-1", "name": "Alice", "email": "alice@test.com", "role": "admin"},
                {"id": "user-2", "name": "Bob", "email": "bob@test.org", "role": "user"},
                {"id": "user-3", "name": "Charlie", "email": "charlie@test.net", "role": "user"}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all", "--include-email", r".*\.org$"])
            assert "Alice" not in result.output
            assert "Bob" in result.output
            assert "Charlie" not in result.output
            assert "Total: 1 users" in result.output
            assert result.exit_code == 0

    def test_users_get_exclude_email_json(self, runner, mock_env):
        """Test users get --all --exclude-email with JSON output."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": "user-1", "name": "Alice", "email": "alice@digitalist.com", "role": "admin"},
                {"id": "user-2", "name": "Bob", "email": "bob@test.com", "role": "user"}
            ]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all", "--exclude-email", "digitalist", "--json"])
            output_data = json.loads(result.output)
            assert len(output_data["users"]) == 1
            assert output_data["users"][0]["email"] == "bob@test.com"
            assert result.exit_code == 0

    def test_users_get_until(self, runner, mock_env):
        """Test users get --all --until excludes users registered after the date."""
        from datetime import datetime
        all_resp = MagicMock()
        all_resp.json.return_value = {"users": [
            {"id": "u1", "name": "Old", "email": "old@test.com", "role": "user"},
            {"id": "u2", "name": "New", "email": "new@test.com", "role": "user"},
        ]}
        page1 = MagicMock()
        page1.json.return_value = {"users": [
            {"id": "u1", "created_at": int(datetime(2026, 8, 31, 23, 0).timestamp())},
            {"id": "u2", "created_at": int(datetime(2026, 9, 1, 0, 30).timestamp())},
        ]}
        empty = MagicMock()
        empty.json.return_value = {"users": []}

        with patch("open_webui_admin.users.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.side_effect = [all_resp, page1, empty]
            mock_get_client.return_value.__enter__ = MagicMock(return_value=mock_client)
            mock_get_client.return_value.__exit__ = MagicMock(return_value=False)

            result = runner.invoke(users, ["get", "--all", "--until", "2026-08-31"])
            assert "Old" in result.output
            assert "New" not in result.output
            assert "Total: 1 users" in result.output
