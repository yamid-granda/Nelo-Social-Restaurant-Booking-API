from rest_framework import viewsets
from reservations.configs import RESERVATION_MAX_THRESHOLD_IN_HOURS
from .serializers import RestaurantSerializer
from .models import Restaurant
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import RestaurantDetailsSerializer, RestaurantSerializer
from datetime import datetime, timedelta
from django.db.models import Q
from base.configs import UTC_FORMAT


def get_date_threshold_limits(str_date: str):
    date = datetime.strptime(str_date, UTC_FORMAT)

    min_limit = (date - timedelta(hours=RESERVATION_MAX_THRESHOLD_IN_HOURS)).strftime(
        UTC_FORMAT
    )

    max_limit = (date + timedelta(hours=RESERVATION_MAX_THRESHOLD_IN_HOURS)).strftime(
        UTC_FORMAT
    )

    return min_limit, max_limit


class RestaurantView(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    filterset_fields = ("name", "tables", "tables__capacity")

    @action(methods=["GET"], detail=False)
    def search(self, request):
        query_params = request.query_params

        datetime_param: str = query_params.get("datetime")
        datetime: str | None = datetime_param if datetime_param else None

        capacity_param: str | None = query_params.get("capacity")
        capacity: int = int(capacity_param) if capacity_param else 1

        diets_param: str | None = query_params.get("diet_ids")
        diet_ids: list[str] = diets_param.split(",") if diets_param else []

        query_filter = Q(tables__capacity__gte=capacity)

        if datetime:
            min_datetime, max_datetime = get_date_threshold_limits(datetime)
            query_filter &= ~Q(
                tables__reservations__datetime__gt=min_datetime,
                tables__reservations__datetime__lt=max_datetime,
            )

        restaurants = Restaurant.objects.filter(query_filter).distinct()

        for diet_id in diet_ids:
            restaurants = restaurants.filter(diets__diet_id=diet_id)

        restaurants = restaurants.order_by("created_at")

        page = self.paginate_queryset(restaurants)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
