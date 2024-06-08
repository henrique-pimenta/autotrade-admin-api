from rest_framework import serializers

from api.apps.vehicle.models import Vehicle


class CreateVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ["id", "status"]


class UpdateVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ["id", "status", "created_at", "updated_at"]


class UpdateVehicleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["id", "status"]
        read_only_fields = ["id"]
