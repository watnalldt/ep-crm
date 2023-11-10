import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    # Test creating a regular user
    email = "test@example.com"
    password = "password123"
    user = User.objects.create_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)
    assert not user.is_staff
    assert not user.is_superuser
    assert user.is_active


@pytest.mark.django_db
def test_create_superuser():
    # Test creating a superuser
    email = "admin@example.com"
    password = "adminpassword123"
    user = User.objects.create_superuser(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)
    assert user.is_staff
    assert user.is_superuser
    assert user.is_active


@pytest.mark.django_db
def test_create_superuser_invalid():
    # Test creating a superuser with invalid fields
    with pytest.raises(ValueError):
        User.objects.create_superuser(email="admin@example.com", password="adminpassword123", is_staff=False)


@pytest.mark.django_db
def test_user_roles():
    # Test setting user roles
    user = User.objects.create_user(email="test@example.com", password="password123", role=User.Roles.ACCOUNT_MANAGER)

    assert user.role == User.Roles.ACCOUNT_MANAGER


@pytest.mark.django_db
def test_user_str_representation():
    # Test the string representation of the User model
    user = User.objects.create_user(email="test@example.com", password="password123")

    assert str(user) == user.email
