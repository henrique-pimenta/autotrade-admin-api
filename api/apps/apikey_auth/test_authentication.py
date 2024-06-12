from unittest import mock

import pytest
from rest_framework.exceptions import AuthenticationFailed

from api.apps.apikey_auth.authentication import ApiKeyAuthentication
from api.apps.apikey_auth.models import ApiKey


@pytest.fixture
def mock_request():
    request = mock.Mock()
    return request


@pytest.fixture
def mock_api_key():
    return "valid_api_key"


@pytest.fixture
def mock_user():
    user = mock.Mock()
    user.username = "testuser"
    return user


def test_authenticate_valid_key(mock_request, mock_api_key, mock_user):
    mock_request.headers = {"Authorization": mock_api_key}

    with mock.patch.object(
        ApiKey.objects, "get", return_value=mock.Mock(user=mock_user)
    ):
        authentication = ApiKeyAuthentication()
        user, _ = authentication.authenticate(mock_request)
        assert user == mock_user


def test_authenticate_missing_key(mock_request):
    mock_request.headers = {}

    authentication = ApiKeyAuthentication()
    with pytest.raises(AuthenticationFailed, match="Missing API key"):
        authentication.authenticate(mock_request)


def test_authenticate_invalid_key(mock_request, mock_api_key):
    mock_request.headers = {"Authorization": mock_api_key}

    with mock.patch.object(ApiKey.objects, "get", side_effect=ApiKey.DoesNotExist):
        authentication = ApiKeyAuthentication()
        with pytest.raises(AuthenticationFailed, match="Invalid API key"):
            authentication.authenticate(mock_request)
