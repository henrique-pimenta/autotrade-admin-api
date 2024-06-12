import pytest

from api.apps.vehicle.models import Vehicle, VehicleStatus
from api.apps.vehicle.serializers import (
    CreateVehicleSerializer,
    UpdateVehicleSerializer,
    UpdateVehicleStatusSerializer,
)


@pytest.mark.django_db
def test_create_vehicle_serializer_valid():
    data = {
        "make": "Ford",
        "model": "Focus",
        "color": "White",
        "year": 2019,
        "kilometerage": 20000,
        "price_cents": 1800000,
    }
    serializer = CreateVehicleSerializer(data=data)
    assert serializer.is_valid()
    vehicle = serializer.save()
    assert vehicle.make == "Ford"
    assert vehicle.model == "Focus"
    assert vehicle.status == VehicleStatus.AVAILABLE.value


@pytest.mark.django_db
def test_create_vehicle_serializer_invalid():
    data = {
        "make": "Ford",
        "model": "Focus",
        "color": "White",
        "year": "not a year",
        "kilometerage": 20000,
        "price_cents": 1800000,
    }
    serializer = CreateVehicleSerializer(data=data)
    assert not serializer.is_valid()
    assert "year" in serializer.errors


@pytest.mark.django_db
def test_update_vehicle_serializer_valid():
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
    data = {
        "make": "Tesla",
        "model": "Model 3",
        "color": "Black",
        "year": 2021,
        "kilometerage": 10000,
        "price_cents": 3500000,
    }
    serializer = UpdateVehicleSerializer(vehicle, data=data)
    assert serializer.is_valid()
    updated_vehicle = serializer.save()
    assert updated_vehicle.make == "Tesla"
    assert updated_vehicle.model == "Model 3"


@pytest.mark.django_db
def test_update_vehicle_serializer_invalid():
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
    data = {
        "year": "not a year",
    }
    serializer = UpdateVehicleSerializer(vehicle, data=data, partial=True)
    assert not serializer.is_valid()
    assert "year" in serializer.errors


@pytest.mark.django_db
def test_update_vehicle_status_serializer_valid():
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
    data = {
        "status": VehicleStatus.SOLD.value,
    }
    serializer = UpdateVehicleStatusSerializer(vehicle, data=data)
    assert serializer.is_valid()
    updated_vehicle = serializer.save()
    assert updated_vehicle.status == VehicleStatus.SOLD.value


@pytest.mark.django_db
def test_update_vehicle_status_serializer_invalid():
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
    data = {
        "status": "not_a_valid_status",
    }
    serializer = UpdateVehicleStatusSerializer(vehicle, data=data)
    assert not serializer.is_valid()
    assert "status" in serializer.errors
