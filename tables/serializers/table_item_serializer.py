from rest_framework import serializers
from ..models import Table
from tables.models import Table


class TableItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = (
            "id",
            "name",
            "capacity",
        )
