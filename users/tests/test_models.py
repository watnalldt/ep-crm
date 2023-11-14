import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import AccountManager, ACManager, CustomUserManager

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    # Test creating a regular user
    email, password = "test@example.com", "password123"
    user = User.objects.create_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)
    assert not user.is_staff and not user.is_superuser
    assert user.is_active


@pytest.mark.django_db
def test_create_superuser():
    # Test creating a superuser
    email, password = "admin@example.com", "adminpassword123"
    user = User.objects.create_superuser(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)
    assert user.is_staff and user.is_superuser and user.is_active


@pytest.mark.django_db
def test_create_superuser_invalid():
    # Test creating a superuser with invalid fields
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="admin@example.com", password="adminpassword123", is_staff=False
        )


@pytest.mark.django_db
def test_user_roles():
    # Test setting user roles
    role = User.Roles.ACCOUNT_MANAGER
    user = User.objects.create_user(email="test@example.com", password="password123", role=role)

    assert user.role == role


@pytest.mark.django_db
def test_user_str_representation():
    # Test the string representation of the User model
    user = User.objects.create_user(email="test@example.com", password="password123")
    assert str(user) == user.email


@pytest.mark.django_db
def test_create_superuser_invalid_flags():
    email, password, role = "admin@example.com", "adminpassword", User.Roles.ADMIN

    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        User.objects.create_superuser(email=email, password=password, role=role, is_staff=False)

    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        User.objects.create_superuser(email=email, password=password, role=role, is_superuser=False)


@pytest.mark.django_db
def test_normalize_email():
    manager = CustomUserManager()
    email = "Test@Example.com"
    normalized_email = manager.normalize_email(email)
    assert normalized_email.lower() == "test@example.com"


@pytest.mark.django_db
def test_returns_email_as_string():
    account_manager = AccountManager(email="test@example.com")
    assert str(account_manager) == "test@example.com"


@pytest.mark.django_db
def test_ac_manager_get_queryset():
    # Test setting user roles
    account_manager = AccountManager.objects.create(
        email="test@example.com", password="testpassword", role="ACCOUNT_MANAGER"
    )

    # Create an instance of ACManager
    account_managers = AccountManager.objects.all()

    # Assert that only users with the ACCOUNT_MANAGER role are in the queryset
    assert account_manager in account_managers

    assert account_managers.count() == 1
