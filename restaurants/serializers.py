from rest_framework import serializers
from .models import Restaurant
from tables.serializers.table_item_serializer import TableItemSerializer
from tables.models import Table
from django.db.models import Q
from reservations.utils import get_limits_from_str_date


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "created_at",
        )


class RestaurantDetailsSerializer(serializers.ModelSerializer):
    tables = TableItemSerializer(many=True, read_only=True)

    def to_representation(self, obj):
        query_params = self.context["request"].query_params
        datetime_param: str = query_params.get("datetime")
        datetime: str | None = datetime_param if datetime_param else None
        data = super().to_representation(obj)

        if datetime:
            min_datetime, max_datetime = get_limits_from_str_date(datetime)

            tables = Table.objects.filter(
                Q(restaurant_id=data["id"])
                & ~Q(
                    reservations__datetime__gt=min_datetime,
                    reservations__datetime__lt=max_datetime,
                )
            )
            data["tables"] = TableItemSerializer(tables, many=True).data

        return data

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "created_at",
            "tables",
        )
