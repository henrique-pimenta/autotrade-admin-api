import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from api.apps.vehicle.models import Vehicle, VehicleStatus


@pytest.mark.django_db
def test_vehicle_creation():
    vehicle = Vehicle.objects.create(
        id="123e4567-e89b-12d3-a456-426614174000",
        status=VehicleStatus.AVAILABLE.value,
        make="Toyota",
        model="Camry",
        color="Blue",
        year=2020,
        kilometerage=15000,
        price_cents=2500000,
    )

    assert vehicle.id == "123e4567-e89b-12d3-a456-426614174000"
    assert vehicle.status == VehicleStatus.AVAILABLE.value
    assert vehicle.make == "Toyota"
    assert vehicle.model == "Camry"
    assert vehicle.color == "Blue"
    assert vehicle.year == 2020
    assert vehicle.kilometerage == 15000
    assert vehicle.price_cents == 2500000


@pytest.mark.django_db
def test_vehicle_status_choices():
    vehicle = Vehicle.objects.create(
        id="123e4567-e89b-12d3-a456-426614174001",
        status=VehicleStatus.SOLD.value,
        make="Honda",
        model="Civic",
        color="Red",
        year=2018,
        kilometerage=30000,
        price_cents=2000000,
    )

    assert vehicle.status == VehicleStatus.SOLD.value


@pytest.mark.django_db
def test_invalid_vehicle_status():
    vehicle = Vehicle(
        id="123e4567-e89b-12d3-a456-426614174002",
        status="invalid",
        make="Ford",
        model="Focus",
        color="White",
        year=2019,
        kilometerage=20000,
        price_cents=1800000,
    )

    with pytest.raises(ValidationError):
        vehicle.full_clean()
        vehicle.save()


@pytest.mark.django_db
def test_vehicle_primary_key():
    vehicle1 = Vehicle.objects.create(
        id="123e4567-e89b-12d3-a456-426614174003",
        status=VehicleStatus.AVAILABLE.value,
        make="Chevrolet",
        model="Impala",
        color="Black",
        year=2021,
        kilometerage=10000,
        price_cents=2700000,
    )

    with pytest.raises(IntegrityError):
        Vehicle.objects.create(
            id=vehicle1.id,
            status=VehicleStatus.AVAILABLE.value,
            make="Chevrolet",
            model="Malibu",
            color="Grey",
            year=2021,
            kilometerage=5000,
            price_cents=2600000,
        )
