import enum
from re import fullmatch
from typing import NamedTuple

from custom_exception import IpAndPortError


class Headers(NamedTuple):
    url: bytes
    slug: bytes


class Value(enum.Enum):
    LISTEN_NUMS = 4
    MIN_PORT = 0
    MAX_PORT = 65535


def get_slug(url: bytes) -> Headers:
    try:
        _, *url_data, _ = url.split(b'/')
        if len(url_data) == 2:
            return Headers(*url_data)

    except ValueError as e:
        raise e


def validate_url(value: str) -> bool:
    """Проверяет соответствие переданного ip адреса установленным правилам написания ip"""
    regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    match = fullmatch(regex, value)
    return True if value == 'localhost' else bool(match)


def check_params(url: str, port: int) -> bool | None:
    """Проверяет переданные параметры ссылки и порта."""
    if not validate_url(url):
        raise IpAndPortError('Неправильно задан url')
    check_value = Value.MIN_PORT.value < port <= Value.MAX_PORT.value
    if not isinstance(port, int) | check_value:
        raise IpAndPortError('Неправильно задан port')
    else:
        return True
