from django.core.management import call_command
import json
from rest_framework import status
from reservations.models import Reservation
from rest_framework.test import APITestCase


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
def http_post(self, body):
    response = self.client.post(self.url, body)
    data = json.loads(response.content)
    return data, response


# data load
def load_initial_data():
    for path in initial_data_paths:
        call_command("loaddata", path, verbosity=0)


# initial data
GLUTEN_FREE = "Gluten Free"
VEGETARIAN = "Vegetarian"
PALEO = "Paleo"
VEGAN = "Vegan"


def get_initial_tables():
    tables_initial_data = open(tables_initial_data_path)
    return json.load(tables_initial_data)


def get_initial_diets():
    diets_initial_data = open(diets_initial_data_path)
    return json.load(diets_initial_data)


def get_diet_ids_by_names(names: list[str]) -> str:
    diets = get_initial_diets()
    diet_ids = [diet["pk"] for diet in diets if diet["fields"]["name"] in names]
    return " ".join(diet_ids)
