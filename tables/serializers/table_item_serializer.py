from rest_framework import serializers
from ..models import Table

from reservations.serializers.reservation_item_serializer import (
    ReservationItemSerializer,
)


class TableItemSerializer(serializers.ModelSerializer):
    reservations = ReservationItemSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = (
            "id",
            "name",
            "capacity",
            "reservations",
        )
