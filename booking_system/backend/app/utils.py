import hashlib
import hmac
import secrets
import string
from datetime import datetime, timedelta

from .config import APP_SECRET


def gen_code(prefix: str = "M", size: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return f"{prefix}{''.join(secrets.choice(alphabet) for _ in range(size))}"


def hash_password(raw_password: str) -> str:
    digest = hmac.new(APP_SECRET.encode("utf-8"), raw_password.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"sha256${digest}"


def verify_password(raw_password: str, stored_value: str) -> bool:
    if stored_value.startswith("sha256$"):
        expected = hash_password(raw_password)
        return hmac.compare_digest(expected, stored_value)

    return hmac.compare_digest(raw_password, stored_value)


def parse_datetime_local(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M")


def split_slots(day_str: str, start_hm: str, end_hm: str, duration_minutes: int):
    day = datetime.strptime(day_str, "%Y-%m-%d").date()
    start = datetime.strptime(start_hm, "%H:%M")
    end = datetime.strptime(end_hm, "%H:%M")

    slots = []
    cur = start
    while cur + timedelta(minutes=duration_minutes) <= end:
        nxt = cur + timedelta(minutes=duration_minutes)
        slots.append((day, cur.strftime("%H:%M"), nxt.strftime("%H:%M")))
        cur = nxt

    return slots
