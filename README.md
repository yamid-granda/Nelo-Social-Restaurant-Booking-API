# Yamid Granda Code Challenge

Check the 👉👉👉 [DEMO Video Here]() 👈👈👈

## Requirements

- `python 3.12.4` or higher
- `pip 24.0` or higher

## Setup Python virtual environment

```sh
pip install virtualenv
python -m venv venv
```

Hint: remember select the virtual python interpreter (`(venv)` prefix)

## Install dependencies

```sh
pip install -r requirements.txt
```

## Create Database Migrations

```sh
python manage.py migrate
```

## Load Initial Data

```sh
python manage.py loaddata initial-data
```

## Run Development Environment

```sh
python manage.py runserver
# go to http://localhost:8000/restaurants/api/v1/restaurants/
```

## Run Unit tests

```sh
python manage.py test
```
