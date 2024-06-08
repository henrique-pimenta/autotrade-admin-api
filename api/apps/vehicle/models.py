from enum import Enum

from django.db import models

from api.shared.mixins import TimestampMixin


class VehicleStatus(Enum):
    AVAILABLE = "available"
    SOLD = "sold"


class Vehicle(TimestampMixin):
    id = models.CharField(max_length=36, primary_key=True)
    status = models.CharField(
        max_length=9,
        choices=[(status.value, status.value) for status in VehicleStatus],
        default=VehicleStatus.AVAILABLE.value,
    )
    make = models.CharField(max_length=36)
    model = models.CharField(max_length=36)
    color = models.CharField(max_length=36)
    year = models.IntegerField()
    kilometerage = models.IntegerField()
    price_cents = models.IntegerField()
