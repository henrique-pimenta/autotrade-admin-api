from django.urls import path

from api.apps.vehicle.views import (
    CreateVehicleView,
    UpdateVehicleStatusView,
    UpdateVehicleView,
)


urlpatterns = [
    path("", CreateVehicleView.as_view(), name="create"),
    path("<str:id>/", UpdateVehicleView.as_view(), name="update"),
    path(
        "<str:id>/update-status/",
        UpdateVehicleStatusView.as_view(),
        name="update status",
    ),
]
