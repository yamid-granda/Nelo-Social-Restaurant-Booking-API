from rest_framework import viewsets
from .serializers.default_serializer import ReservationSerializer
from .models import Reservation
from rest_framework.exceptions import ValidationError
from base.utils import get_utc_now
from rest_framework.response import Response
from rest_framework import status
from diets.models import Diet
from tables.models import Table
from restaurants.models import Restaurant
from restaurants_diets.models import RestaurantDiet
from reservations.models import Reservation
from datetime import timedelta
from .configs import RESERVATION_MAX_THRESHOLD_IN_HOURS
from django.db import transaction
from .utils import get_limits_from_date


class ReservationView(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validate_request(request, serializer)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


def validate_request(request, serializer):
    is_future_datetime(serializer)
    is_free_datetime(serializer)
    diets = diets_exist(request)
    table = table_allows_capacity(request, serializer)
    restaurant_allows_diets(diets, table)


# validations
def is_future_datetime(serializer):
    datetime = serializer.validated_data["datetime"]
    utc_now = get_utc_now()

    if datetime <= utc_now:
        raise ValidationError("datetime must be a future date")


def is_free_datetime(serializer):
    datetime = serializer.validated_data["datetime"]
    min_limit, max_limit = get_limits_from_date(datetime)
    table_id = serializer.validated_data["table_id"].id

    try:
        Reservation.objects.get(
            table_id=table_id,
            datetime__gt=min_limit,
            datetime__lt=max_limit,
        )
        raise ValidationError("Datetime is not available")
    except Reservation.DoesNotExist:
        return


def diets_exist(request) -> list[str]:
    if request.data.get("diet_ids") is None:
        return []

    diet_ids = request.data["diet_ids"].split()
    diets = Diet.objects.filter(pk__in=diet_ids)

    if len(diet_ids) != len(diets):
        raise ValidationError("one or more diet ids not exist")

    return diets


def table_allows_capacity(request, serializer):
    quantity = int(request.data.get("quantity", 1))
    table_id = serializer.validated_data["table_id"].id
    table = Table.objects.get(pk=table_id)

    if quantity > table.capacity:
        raise ValidationError(f"The max capacity of the table is {table.capacity}")

    return table


def restaurant_allows_diets(diets, table):
    if len(diets) == 0:
        return

    restaurant = Restaurant.objects.get(pk=table.restaurant_id.id)

    for diet in diets:
        try:
            RestaurantDiet.objects.get(restaurant_id=restaurant.id, diet_id=diet.id)
        except RestaurantDiet.DoesNotExist:
            raise ValidationError(
                f'The restaurant "{restaurant.name}" does not has the {diet.name} diet endorsement'
            )
