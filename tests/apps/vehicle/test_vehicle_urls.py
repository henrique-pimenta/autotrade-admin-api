from unittest.mock import patch
from uuid import uuid4

import pytest
from decouple import config
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.apps.apikey_auth.models import ApiKey
from api.apps.vehicle.models import Vehicle, VehicleStatus


@pytest.mark.django_db
@patch("api.gateways.sales_service.requests.post")
def test_create_vehicle_view(mock_post):
    mock_response = mock_post.return_value
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": "1cb1dd9c-6831-4840-9fb5-aea2620546ae",
        "created_at": "2024-06-11T22:51:55.230361Z",
        "updated_at": "2024-06-11T22:51:55.230361Z",
        "available": True,
        "make": "Ford",
        "model": "Focus",
        "color": "White",
        "year": 2019,
        "kilometerage": 20000,
        "price_cents": 1800000,
    }
    client = APIClient()
    url = reverse("api.apps.vehicle:create")
    data = {
        "make": "Ford",
        "model": "Focus",
        "color": "White",
        "year": 2019,
        "kilometerage": 20000,
        "price_cents": 1800000,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Vehicle.objects.count() == 1
    vehicle = Vehicle.objects.get()
    assert vehicle.make == "Ford"
    assert vehicle.model == "Focus"


@pytest.mark.django_db
@patch("api.gateways.sales_service.requests.patch")
def test_patch_update_vehicle_view(mock_patch):
    mock_response = mock_patch.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "created_at": "2024-06-11T22:51:55.230361Z",
        "updated_at": "2024-06-11T22:51:55.230361Z",
        "available": True,
        "make": "Ford",
        "model": "Focus",
        "color": "White",
        "year": 2019,
        "kilometerage": 20000,
        "price_cents": 1800000,
    }
    vehicle = Vehicle.objects.create(
        id="123e4567-e89b-12d3-a456-426614174000",
        status=VehicleStatus.AVAILABLE.value,
        make="Ford",
        model="Focus",
        color="White",
        year=2019,
        kilometerage=20000,
        price_cents=1800000,
    )
    client = APIClient()
    url = reverse("api.apps.vehicle:update", args=[vehicle.id])
    data = {
        "make": "Tesla",
        "model": "Model 3",
        "color": "Black",
        "year": 2021,
        "kilometerage": 10000,
        "price_cents": 3500000,
    }

    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    vehicle.refresh_from_db()
    assert vehicle.make == "Tesla"
    assert vehicle.model == "Model 3"
    assert vehicle.color == "Black"
    assert vehicle.year == 2021
    assert vehicle.kilometerage == 10000
    assert vehicle.price_cents == 3500000


@pytest.mark.django_db
def test_put_update_vehicle_view():
    vehicle = Vehicle.objects.create(
        id="123e4567-e89b-12d3-a456-426614174000",
        status=VehicleStatus.AVAILABLE.value,
        make="Ford",
        model="Focus",
        color="White",
        year=2019,
        kilometerage=20000,
        price_cents=1800000,
    )
    client = APIClient()
    url = reverse("api.apps.vehicle:update", args=[vehicle.id])
    data = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "created_at": "2024-06-11T22:51:55.230361Z",
        "updated_at": "2024-06-11T22:51:55.230361Z",
        "available": True,
        "make": "Ford",
        "model": "Focus",
        "color": "White",
        "year": 2019,
        "kilometerage": 20000,
        "price_cents": 1000000,
    }

    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_update_vehicle_status_view():
    mock_sales_service_user = User.objects.create(username="mock_sales_service")
    api_key = ApiKey.objects.create(user=mock_sales_service_user, key=str(uuid4()))
    vehicle = Vehicle.objects.create(
        id="123e4567-e89b-12d3-a456-426614174000",
        status=VehicleStatus.AVAILABLE.value,
        make="Ford",
        model="Focus",
        color="White",
        year=2019,
        kilometerage=20000,
        price_cents=1800000,
    )
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=api_key.key)
    url = reverse("api.apps.vehicle:update status", args=[vehicle.id])
    data = {
        "status": VehicleStatus.SOLD.value,
    }

    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    vehicle.refresh_from_db()
    assert vehicle.status == VehicleStatus.SOLD.value
