from datetime import datetime, timedelta
from base.configs import UTC_FORMAT
from reservations.configs import RESERVATION_MAX_THRESHOLD_IN_HOURS as MAX_THRESHOLD


def get_limits_from_str_date(str_date: str):
    date = datetime.strptime(str_date, UTC_FORMAT)
    min_limit = (date - timedelta(hours=MAX_THRESHOLD)).strftime(UTC_FORMAT)
    max_limit = (date + timedelta(hours=MAX_THRESHOLD)).strftime(UTC_FORMAT)
    return min_limit, max_limit
