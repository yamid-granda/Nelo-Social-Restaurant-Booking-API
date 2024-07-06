from rest_framework import serializers
from .models import Reservation
from restaurants.serializers import RestaurantSerializer


class ReservationSerializer(serializers.ModelSerializer):
    table_id = RestaurantSerializer

    class Meta:
        model = Reservation
        fields = (
            "id",
            "datetime",
            "quantity",
            "table_id",
            "created_at",
        )
