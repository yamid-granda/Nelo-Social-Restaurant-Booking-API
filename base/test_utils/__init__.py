from django.core.management import call_command
import json
from rest_framework.test import APITestCase
from functools import reduce
from datetime import datetime
from base.configs import UTC_FORMAT

restaurants_initial_data_path = "restaurants/fixtures/initial-data.json"
diets_initial_data_path = "diets/fixtures/initial-data.json"
restaurants_diets_initial_data_path = "restaurants_diets/fixtures/initial-data.json"
tables_initial_data_path = "tables/fixtures/initial-data.json"

initial_data_paths = [
    restaurants_initial_data_path,
    diets_initial_data_path,
    restaurants_diets_initial_data_path,
    tables_initial_data_path,
]


# http
def http_get(self: APITestCase, query_params=None):
    response = self.client.get(self.url, query_params)
    data = json.loads(response.content)
    return data, response


def http_post(self: APITestCase, body, url=None):
    response = self.client.post(url or self.url, body)
    data = json.loads(response.content)
    return data, response


# data load
def load_initial_data():
    for path in initial_data_paths:
        call_command("loaddata", path, verbosity=0)


# initial data
def get_initial_tables():
    tables_initial_data = open(tables_initial_data_path)
    return json.load(tables_initial_data)


def get_initial_diets():
    diets_initial_data = open(diets_initial_data_path)
    return json.load(diets_initial_data)


def get_initial_restaurants():
    restaurants_initial_data = open(restaurants_initial_data_path)
    return json.load(restaurants_initial_data)


def get_diet_ids_by_names(names: list[str]) -> str:
    diets = get_initial_diets()
    diet_ids = [diet["pk"] for diet in diets if diet["fields"]["name"] in names]
    return " ".join(diet_ids)


def get_restaurants_by_names(names: list[str], capacity: int = 1):
    restaurants = get_initial_restaurants()

    def reducer(acc, restaurant):
        restaurant_name = restaurant["fields"]["name"]
        if restaurant_name in names:
            table_fixtures = get_restaurant_table_fixtures(restaurant_name, capacity)
            tables = [*map(get_table_from_fixture, table_fixtures)]

            acc.append(
                {
                    "id": restaurant["pk"],
                    "name": restaurant["fields"]["name"],
                    "created_at": restaurant["fields"]["created_at"],
                    "tables": tables,
                }
            )
        return acc

    return reduce(reducer, restaurants, [])


def get_diets_ids_by_names(names: list[str]) -> str:
    diets = get_initial_diets()
    diet_ids = [diet["pk"] for diet in diets if diet["fields"]["name"] in names]
    return ",".join(diet_ids)


def get_restaurant_by_name(name: str):
    restaurants = get_initial_restaurants()
    return next(
        restaurant for restaurant in restaurants if restaurant["fields"]["name"] == name
    )


def get_restaurant_table_fixtures(name: str, capacity: int = 1) -> list[dict]:
    restaurant = get_restaurant_by_name(name)
    table_fixtures = get_initial_tables()
    tables = []

    for table in table_fixtures:
        restaurant_id = table["fields"]["restaurant_id"]
        table_capacity = table["fields"]["capacity"]
        if restaurant_id == restaurant["pk"] and table_capacity >= capacity:
            tables.append(table)

    return tables


def get_table_from_fixture(fixture: dict):
    return {
        "id": fixture["pk"],
        "name": fixture["fields"]["name"],
        "capacity": fixture["fields"]["capacity"],
    }


def reserve_restaurant_datetime(
    self, restaurant_name: str, datetime: datetime, is_full=True
) -> None:
    url = "/reservations/api/v1/reservations/"
    body_base = {"datetime": datetime, "made_out_to": "Test User"}
    restaurant_tables = get_restaurant_table_fixtures(restaurant_name)

    if not is_full:
        restaurant_tables = restaurant_tables[1:]

    for table in restaurant_tables:
        http_post(self, {**body_base, "table_id": table["pk"]}, url)


# diets
INITIAL_DIETS_FIXTURE = get_initial_diets()

GLUTEN_FREE = INITIAL_DIETS_FIXTURE[0]["fields"]["name"]
PALEO = INITIAL_DIETS_FIXTURE[1]["fields"]["name"]
VEGETARIAN = INITIAL_DIETS_FIXTURE[2]["fields"]["name"]
VEGAN = INITIAL_DIETS_FIXTURE[3]["fields"]["name"]

# restaurants
INITIAL_RESTAURANTS_FIXTURE = get_initial_restaurants()

LARDO = INITIAL_RESTAURANTS_FIXTURE[0]["fields"]["name"]
PANADERIA_ROSETTA = INITIAL_RESTAURANTS_FIXTURE[1]["fields"]["name"]
TETETLAN = INITIAL_RESTAURANTS_FIXTURE[2]["fields"]["name"]
FALLING_PIANO_BREWING_CO = INITIAL_RESTAURANTS_FIXTURE[3]["fields"]["name"]
U_TO_PI_A = INITIAL_RESTAURANTS_FIXTURE[4]["fields"]["name"]


ALL_RESTAURANTS = get_restaurants_by_names(
    [
        LARDO,
        PANADERIA_ROSETTA,
        TETETLAN,
        FALLING_PIANO_BREWING_CO,
        U_TO_PI_A,
    ]
)


# date
def parse_date_to_db_format(str_date: datetime) -> str:
    return str_date.strftime(UTC_FORMAT)


# utils
def assert_lists_are_equal(self: APITestCase, list1: list, list2: list):
    self.assertEqual(
        sorted(list1, key=lambda x: x["id"]), sorted(list2, key=lambda x: x["id"])
    )
