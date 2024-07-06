from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from dateutil import parser
from datetime import timedelta, datetime
from base.test_utils import (
    GLUTEN_FREE,
    VEGETARIAN,
    PALEO,
    VEGAN,
    get_diet_ids_by_names,
    load_initial_data,
    get_initial_tables,
    http_post,
    get_initial_diets,
)
from base.utils import get_utc_now
from .models import Reservation
from .configs import RESERVATION_MAX_THRESHOLD_IN_HOURS


# configs
tables = get_initial_tables()
table_1_panaderia_rosetta = tables[0]
table_1_panaderia_rosetta_id = table_1_panaderia_rosetta["pk"]
diets = get_initial_diets()
utc_now = get_utc_now()
future_utc_date = utc_now + timedelta(days=1)

body_base = {
    "table_id": table_1_panaderia_rosetta_id,
    "datetime": future_utc_date,
}

expected_response_keys = ["id", "datetime", "quantity", "table_id", "created_at"]


class TestConfig(APITestCase):
    # before each
    def setUp(self):
        self.client = APIClient()
        self.url = "/reservations/api/v1/reservations/"
        load_initial_data()

    # utils
    def assert_creation(
        self,
        http_response,
        datetime=future_utc_date,
        quantity: int = 1,
        reservations_count=1,
    ):
        data, response = http_response

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), reservations_count)
        self.assertEqual([*data.keys()], expected_response_keys)

        datetime_response = parser.parse(data["datetime"])
        self.assertEqual(datetime_response, datetime)
        self.assertEqual(data["quantity"], quantity)


# creation test cases
class CreateToSpecificDates(TestConfig):
    # success cases
    def test_create_to_future_date(self):
        # GIVEN
        self.assertEqual(Reservation.objects.count(), 0)
        body = body_base

        # WHEN
        response = http_post(self, body)

        # THEN
        self.assert_creation(response)

    def test_create_in_threshold(self):
        # GIVEN
        http_post(self, body_base)
        two_hours_after = future_utc_date + timedelta(
            hours=RESERVATION_MAX_THRESHOLD_IN_HOURS
        )

        # WHEN
        response = http_post(self, {**body_base, "datetime": two_hours_after})

        # THEN
        self.assert_creation(response, reservations_count=2, datetime=two_hours_after)

    # failure cases
    def test_create_in_past_date(self):
        # GIVEN
        past_utc_date = utc_now + timedelta(seconds=-1)
        body = {**body_base, "datetime": past_utc_date}

        # WHEN
        data, response = http_post(self, body)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data, ["datetime must be a future date"])

    def test_create_in_same_table_reservation_date(self):
        # GIVEN
        http_post(self, body_base)

        # WHEN
        data, response = http_post(self, body_base)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data, ["Datetime is not available"])

    def test_create_inside_the_allowed_threshold(self):
        # GIVEN
        http_post(self, body_base)
        two_hours_after = future_utc_date + timedelta(
            hours=RESERVATION_MAX_THRESHOLD_IN_HOURS, seconds=-1
        )

        # WHEN
        data, response = http_post(self, {**body_base, "datetime": two_hours_after})

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data, ["Datetime is not available"])


class CreateWithDietaryRestrictions(TestConfig):
    # success cases
    def test_1_dietary_restriction(self):
        # GIVEN
        diet_ids = get_diet_ids_by_names([GLUTEN_FREE])
        body = {**body_base, "diet_ids": diet_ids}

        # WHEN
        response = http_post(self, body)

        # THEN
        self.assert_creation(response)

    def test_2_dietary_restrictions(self):
        # GIVEN
        diet_ids = get_diet_ids_by_names([GLUTEN_FREE, VEGETARIAN])
        body = {**body_base, "diet_ids": diet_ids}

        # WHEN
        response = http_post(self, body)

        # THEN
        self.assert_creation(response)

    # failure cases
    def test_dietary_not_supported(self):
        # GIVEN
        self.assertEqual(Reservation.objects.count(), 0)
        diet_ids = get_diet_ids_by_names([PALEO])
        body = {**body_base, "diet_ids": diet_ids}

        # WHEN
        data, response = http_post(self, body)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = [
            f'The restaurant "Panadería Rosetta" does not has the {PALEO} diet endorsement'
        ]
        self.assertEqual(data, expected_error)

    def test_1_dietary_not_supported_1_dietary_supported(self):
        # GIVEN
        diet_ids = get_diet_ids_by_names([VEGETARIAN, VEGAN])
        body = {**body_base, "diet_ids": diet_ids}

        # WHEN
        data, response = http_post(self, body)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = [
            f'The restaurant "Panadería Rosetta" does not has the {VEGAN} diet endorsement'
        ]
        self.assertEqual(data, expected_error)

    def test_1_dietary_not_supported_2_dietary_supported(self):
        # GIVEN
        diet_ids = get_diet_ids_by_names([PALEO, GLUTEN_FREE, VEGETARIAN])
        body = {**body_base, "diet_ids": diet_ids}

        # WHEN
        data, response = http_post(self, body)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = [
            f'The restaurant "Panadería Rosetta" does not has the {PALEO} diet endorsement'
        ]
        self.assertEqual(data, expected_error)


class CreateToMultipleDiners(TestConfig):
    # success cases
    def test_fill_the_table_capacity(self):
        # GIVEN
        quantity = 2
        body = {**body_base, "quantity": quantity}

        # WHEN
        response = http_post(self, body)

        # THEN
        self.assert_creation(response, quantity=quantity)

    # failure cases
    def test_exceed_table_capacity(self):
        # GIVEN
        body = {**body_base, "quantity": 3}

        # WHEN
        data, response = http_post(self, body)

        # THEN
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error = ["The max capacity of the table is 2"]
        self.assertEqual(data, expected_error)
