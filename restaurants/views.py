from rest_framework import viewsets
from .serializers import RestaurantSerializer
from .models import Restaurant
from rest_framework.decorators import action
from .serializers import RestaurantDetailsSerializer, RestaurantSerializer
from django.db.models import Q
from reservations.utils import get_limits_from_str_date


class RestaurantView(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    filterset_fields = ("name", "tables", "tables__capacity")

    @action(methods=["GET"], detail=False)
    def details(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = RestaurantDetailsSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

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
            min_datetime, max_datetime = get_limits_from_str_date(datetime)
            query_filter &= ~Q(
                tables__reservations__datetime__gt=min_datetime,
                tables__reservations__datetime__lt=max_datetime,
            )

        restaurants = Restaurant.objects.filter(query_filter).distinct()

        for diet_id in diet_ids:
            restaurants = restaurants.filter(diets__diet_id=diet_id)

        restaurants = restaurants.order_by("created_at")

        page = self.paginate_queryset(restaurants)
        serializer = RestaurantDetailsSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)
