# Yamid Granda Code Challenge

Check the 👉👉👉 [DEMO Video Here](https://drive.google.com/file/d/1lyguTMN25EDdGSXDgnvPzfBkUMYFUIwD/view?usp=sharing) 👈👈👈

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

## Migrate Database

```sh
python manage.py migrate
```

## Load Initial Data

```sh
python manage.py loaddata initial-data
```

## Launch Development Environment

```sh
python manage.py runserver
# go to http://localhost:8000/restaurants/api/v1/restaurants/
```

## Unit Tests

```sh
python manage.py test
```

## API E2E (End to End) Tests

### E2E Environment Requirements

- `node 20` or higher
- `npm 8.1` or higher

### Run E2E Tests

1. Go to `./e2e-tests` folder
2. Install dependencies `npm install` or `pnpm install` (recommended)
3. **Important:** make sure the Django server is running in the root folder `python manage.py runserver`
4. Run the tests

```sh
npm run test
# or
pnpm test
```

## Architecture

Check the Database Model in the `database-model.drawio` file

## Useful Endpoints

- Search Restaurants: `http://127.0.0.1:8000/restaurants/api/v1/restaurants/search/?capacity=4&diet_ids=0a15355d-26fc-4793-8f74-e51b0aa1d968,891efe06-d6da-41ac-92aa-90f0625cc519&datetime=2024-07-17T10:01:00.000Z`
- Reservations CRUD: `http://127.0.0.1:8000/reservations/api/v1/reservations/`
- Restaurants CRUD: `http://127.0.0.1:8000/restaurants/api/v1/restaurants/`
- Diets CRUD: `http://127.0.0.1:8000/diets/api/v1/diets/`
- Tables CRUD: `http://127.0.0.1:8000/tables/api/v1/tables/`
- Restaurants Diets CRUD: `http://127.0.0.1:8000/restaurants-diets/api/v1/restaurants-diets/`
