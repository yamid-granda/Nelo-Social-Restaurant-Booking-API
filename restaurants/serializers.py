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

        capacity_param: str | None = query_params.get("capacity")
        capacity: int = int(capacity_param) if capacity_param else 1

        data = super().to_representation(obj)
        filter_query = Q(restaurant_id=data["id"], capacity__gte=capacity)

        if datetime:
            min_datetime, max_datetime = get_limits_from_str_date(datetime)
            filter_query &= ~Q(
                reservations__datetime__gt=min_datetime,
                reservations__datetime__lt=max_datetime,
            )

        tables = Table.objects.filter(filter_query)
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
