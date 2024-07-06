from rest_framework import serializers
from .models import RestaurantDiet
from restaurants.serializers import RestaurantSerializer
from diets.serializers import DietSerializer


class RestaurantDietSerializer(serializers.ModelSerializer):
    restaurant_id = RestaurantSerializer
    diet_id = DietSerializer

    class Meta:
        model = RestaurantDiet
        fields = (
            "id",
            "created_at",
            "restaurant_id",
            "diet_id",
        )
