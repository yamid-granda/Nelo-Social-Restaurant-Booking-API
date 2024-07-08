from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from base.utils import get_utc_now
from base.test_utils import (
    get_initial_tables,
    get_restaurants_by_names,
    http_get,
    assert_lists_are_equal,
    load_initial_data,
    get_diets_ids_by_names,
    parse_date_to_db_format,
    ALL_RESTAURANTS,
    PANADERIA_ROSETTA,
    FALLING_PIANO_BREWING_CO,
    LARDO,
    U_TO_PI_A,
    TETETLAN,
    GLUTEN_FREE,
    PALEO,
    VEGETARIAN,
    VEGAN,
    reserve_restaurant_datetime,
)
from uuid import uuid4
from django.core.management import call_command
from copy import deepcopy

tables = get_initial_tables()
utc_now = get_utc_now()

tomorrow_at_18h: str = parse_date_to_db_format(
    datetime(utc_now.year, utc_now.month, utc_now.day, 18, 0) + timedelta(days=1)
)

tomorrow_at_18h_00m_01s: str = parse_date_to_db_format(
    datetime(utc_now.year, utc_now.month, utc_now.day, 18, 0, 1) + timedelta(days=1)
)

tomorrow_at_19h_59m_59s: str = parse_date_to_db_format(
    datetime(utc_now.year, utc_now.month, utc_now.day, 19, 59, 59) + timedelta(days=1)
)

tomorrow_at_20h: str = parse_date_to_db_format(
    datetime(utc_now.year, utc_now.month, utc_now.day, 20, 0) + timedelta(days=1)
)

tomorrow_at_22h = parse_date_to_db_format(
    datetime(utc_now.year, utc_now.month, utc_now.day, 22, 0) + timedelta(days=1)
)

tomorrow_at_21h_59m_59s = parse_date_to_db_format(
    datetime(utc_now.year, utc_now.month, utc_now.day, 21, 59, 59) + timedelta(days=1)
)


class TestConfig(APITestCase):
    # before each
    def setUp(self):
        self.client = APIClient()
        self.url = "/restaurants/api/v1/restaurants/search/"
        load_initial_data()


class QueryRestaurants(TestConfig):
    def test_no_params_paginated_response(self):
        # WHEN
        data, response = http_get(self)

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            data,
            {
                "count": 5,
                "next": None,
                "previous": None,
                "results": ALL_RESTAURANTS,
            },
        )


class QueryRestaurantsByCapacity(TestConfig):
    def test_less_than_min_capacity(self):
        # GIVEN
        query_params = {"capacity": 1}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(self, data["results"], ALL_RESTAURANTS)

    def test_min_capacity(self):
        # GIVEN
        query_params = {"capacity": 2}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(self, data["results"], ALL_RESTAURANTS)

    def test_mid_capacity(self):
        # GIVEN
        capacity = 4
        query_params = {"capacity": capacity}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names(
                [PANADERIA_ROSETTA, LARDO, TETETLAN, FALLING_PIANO_BREWING_CO], capacity
            ),
        )

    def test_max_capacity(self):
        # GIVEN
        capacity = 6
        query_params = {"capacity": capacity}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names(
                [LARDO, TETETLAN, FALLING_PIANO_BREWING_CO], capacity
            ),
        )

    def test_exceed_max_capacity(self):
        # GIVEN
        query_params = {"capacity": 7}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(self, data["results"], [])


class QueryRestaurantsByDietIds(TestConfig):
    def test_1_diet(self):
        # GIVEN
        query_params = {"diet_ids": get_diets_ids_by_names([GLUTEN_FREE])}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names([LARDO, PANADERIA_ROSETTA, TETETLAN]),
        )

    def test_2_diets(self):
        # GIVEN
        query_params = {"diet_ids": get_diets_ids_by_names([VEGAN, VEGETARIAN])}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names([U_TO_PI_A]),
        )

    def test_diets_not_match(self):
        # GIVEN
        query_params = {"diet_ids": get_diets_ids_by_names([PALEO, VEGETARIAN])}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(self, data["results"], [])

    def test_fake_diet_id(self):
        # GIVEN
        query_params = {"diet_ids": uuid4()}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(self, data["results"], [])


class QueryRestaurantsByCapacityAndDietIds(TestConfig):
    def test_capacity_and_diet(self):
        # GIVEN
        capacity = 4
        query_params = {
            "capacity": 4,
            "diet_ids": get_diets_ids_by_names([VEGETARIAN]),
        }

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names([PANADERIA_ROSETTA], capacity),
        )

    def test_capacity_and_2_diets(self):
        # GIVEN
        capacity = 6
        query_params = {
            "capacity": capacity,
            "diet_ids": get_diets_ids_by_names([PALEO, GLUTEN_FREE]),
        }

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names([TETETLAN], capacity),
        )

    def test_capacity_and_diet_with_multiple_results(self):
        # GIVEN
        capacity = 6
        query_params = {
            "capacity": capacity,
            "diet_ids": get_diets_ids_by_names([GLUTEN_FREE]),
        }

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names([TETETLAN, LARDO], capacity),
        )


class QueryRestaurantsByDatetime(TestConfig):
    def test_restaurant_all_tables_free_at_all_datetimes(self):
        # GIVEN
        query_params = {"datetime": tomorrow_at_20h}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(self, data["results"], ALL_RESTAURANTS)

    def test_not_available_restaurant_at_datetime(self):
        # GIVEN
        reserve_restaurant_datetime(self, PANADERIA_ROSETTA, tomorrow_at_20h)
        query_params = {"datetime": tomorrow_at_20h}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names(
                [
                    LARDO,
                    TETETLAN,
                    FALLING_PIANO_BREWING_CO,
                    U_TO_PI_A,
                ]
            ),
        )

    def test_1_available_restaurant_table_at_datetime(self):
        # GIVEN
        reserve_restaurant_datetime(
            self, PANADERIA_ROSETTA, tomorrow_at_20h, is_full=False
        )
        query_params = {"datetime": tomorrow_at_20h}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        expected_result = deepcopy(ALL_RESTAURANTS)
        expected_result[1]["tables"] = expected_result[1]["tables"][:1]
        assert_lists_are_equal(self, data["results"], expected_result)

    # threshold limits
    def test_available_at_threshold_bottom(self):
        # GIVEN
        reserve_restaurant_datetime(self, PANADERIA_ROSETTA, tomorrow_at_20h)
        query_params = {"datetime": tomorrow_at_18h}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(self, data["results"], ALL_RESTAURANTS)

    def test_not_available_at_threshold_bottom(self):
        # GIVEN
        reserve_restaurant_datetime(self, PANADERIA_ROSETTA, tomorrow_at_20h)
        query_params = {"datetime": tomorrow_at_18h_00m_01s}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names(
                [
                    LARDO,
                    TETETLAN,
                    FALLING_PIANO_BREWING_CO,
                    U_TO_PI_A,
                ]
            ),
        )

    def test_not_available_before_threshold(self):
        # GIVEN
        reserve_restaurant_datetime(self, PANADERIA_ROSETTA, tomorrow_at_20h)
        query_params = {"datetime": tomorrow_at_19h_59m_59s}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names(
                [
                    LARDO,
                    TETETLAN,
                    FALLING_PIANO_BREWING_CO,
                    U_TO_PI_A,
                ]
            ),
        )

    def test_not_available_at_threshold_top_limit(self):
        # GIVEN
        reserve_restaurant_datetime(self, PANADERIA_ROSETTA, tomorrow_at_20h)
        query_params = {"datetime": tomorrow_at_21h_59m_59s}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(
            self,
            data["results"],
            get_restaurants_by_names(
                [
                    LARDO,
                    TETETLAN,
                    FALLING_PIANO_BREWING_CO,
                    U_TO_PI_A,
                ]
            ),
        )

    def test_available_after_threshold(self):
        # GIVEN
        reserve_restaurant_datetime(self, PANADERIA_ROSETTA, tomorrow_at_20h)
        query_params = {"datetime": tomorrow_at_22h}

        # WHEN
        data, _ = http_get(self, query_params)

        # THEN
        assert_lists_are_equal(self, data["results"], ALL_RESTAURANTS)
