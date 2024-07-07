from rest_framework import serializers
from ..models import Reservation


class ReservationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = (
            "id",
            "datetime",
            "quantity",
            "created_at",
        )
