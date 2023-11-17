import pytest
from django.urls import reverse
from model_bakery import baker

from clients.models import Client  # Adjust the import path accordingly


@pytest.fixture
def account_manager():
    return baker.make("AccountManager")


@pytest.fixture
def client(account_manager):
    return baker.make("Client", account_manager=account_manager)


@pytest.mark.django_db
def test_client_model(client):
    assert Client.objects.count() == 1
    assert str(client) == client.client
    assert client.get_absolute_url() == reverse("clients:client_contracts", args=[str(client.pk)])


@pytest.mark.django_db
def test_client_unique_constraint(account_manager):
    # Test that the unique constraint on the client field is enforced
    client1 = baker.make("Client", account_manager=account_manager)
    with pytest.raises(Exception):
        baker.make("Client", client=client1.client, account_manager=account_manager)
