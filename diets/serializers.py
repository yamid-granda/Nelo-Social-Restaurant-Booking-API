from rest_framework import serializers
from .models import Diet


class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = (
            "id",
            "name",
            "created_at",
        )
