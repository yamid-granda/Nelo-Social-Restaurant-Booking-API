from rest_framework import serializers
from ..models import RestaurantDiet
from diets.serializers import DietSerializer


class RestaurantDietItemSerializer(serializers.ModelSerializer):
    diet_id = DietSerializer

    class Meta:
        model = RestaurantDiet
        fields = (
            "id",
            "created_at",
            "restaurant_id",
            "diet_id",
        )
