from rest_framework import serializers
from .models import Restaurant
from tables.serializers.table_item_serializer import TableItemSerializer
from restaurants_diets.serializers.restaurant_diet_item_serializer import (
    RestaurantDietItemSerializer,
)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "created_at",
        )


class RestaurantDetailsSerializer(serializers.ModelSerializer):
    diets = RestaurantDietItemSerializer(many=True, read_only=True)
    tables = TableItemSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "created_at",
            "diets",
            "tables",
        )
