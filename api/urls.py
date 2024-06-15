from django.contrib import admin
from django.urls import path, include

from api.apps.vehicle.views import LoginView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "api/vehicles/",
        include(("api.apps.vehicle.urls", "vehicle"), namespace="api.apps.vehicle"),
    ),
]
