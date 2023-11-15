import pytest

from clients.models import Client
from users.models import AccountManager


@pytest.mark.django_db
def test_create_new_client_with_valid_data():
    account_manager = AccountManager.objects.create(
        email="testuser@example.com", password="1245679", role="ACCOUNT_MANAGER"
    )
    client_data = {
        "client": "TestClient",
        "account_manager": account_manager,
    }
    client = Client.objects.create(**client_data)
    assert isinstance(client, Client)
    assert str(client) == "TestClient"
