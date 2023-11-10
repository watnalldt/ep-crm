# tests/test_models.py
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        is_staff=False,
        is_admin=False,
        is_active=True,
        date_joined=timezone.now(),
        role=User.Roles.ACCOUNT_MANAGER,
    )

    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert not user.is_staff
    assert not user.is_admin
    assert user.is_active
    assert user.date_joined is not None
    assert user.role == User.Roles.ACCOUNT_MANAGER


@pytest.mark.django_db
def test_user_str_representation():
    user = User.objects.create(
        email="test@example.com", first_name="John", last_name="Doe", role=User.Roles.CLIENT_MANAGER
    )

    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test_user_roles():
    assert User.Roles.ACCOUNT_MANAGER == "ACCOUNT_MANAGER"
    assert User.Roles.CLIENT_MANAGER == "CLIENT_MANAGER"
    assert User.Roles.ADMIN == "ADMIN"
