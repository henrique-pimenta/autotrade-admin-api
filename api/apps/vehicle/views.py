import uuid

from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.apps.apikey_auth.authentication import ApiKeyAuthentication
from api.apps.vehicle.models import Vehicle
from api.apps.vehicle.serializers import (
    CreateVehicleSerializer,
    UpdateVehicleSerializer,
    UpdateVehicleStatusSerializer,
)
from api.gateways import sales_service


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return Response({"csrfToken": csrf_token}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class CreateVehicleView(CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = CreateVehicleSerializer

    def post(self, request, *args, **kwargs):
        data = {
            "make": request.data.get("make"),
            "model": request.data.get("model"),
            "color": request.data.get("color"),
            "year": request.data.get("year"),
            "kilometerage": request.data.get("kilometerage"),
            "price_cents": request.data.get("price_cents"),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(id=str(uuid.uuid4()), status="available")
        headers = self.get_success_headers(serializer.data)

        sales_service.create_vehicle(request_body=dict(serializer.data))

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UpdateVehicleView(UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = UpdateVehicleSerializer
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        sales_service.update_vehicle(request_body=dict(response.data))
        return response


class UpdateVehicleStatusView(UpdateAPIView):
    authentication_classes = [ApiKeyAuthentication]
    queryset = Vehicle.objects.all()
    serializer_class = UpdateVehicleStatusSerializer
    lookup_field = "id"
