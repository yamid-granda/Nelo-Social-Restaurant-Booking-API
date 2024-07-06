from datetime import datetime, timezone


def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)
