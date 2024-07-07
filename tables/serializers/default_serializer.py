from rest_framework import serializers
from ..models import Table
from restaurants.serializers import RestaurantSerializer


class TableSerializer(serializers.ModelSerializer):
    restaurant_id = RestaurantSerializer

    class Meta:
        model = Table
        fields = (
            "id",
            "restaurant_id",
            "name",
            "capacity",
            "created_at",
        )
