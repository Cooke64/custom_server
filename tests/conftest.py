import pytest

from src.client_part_class import BaseHandler


@pytest.fixture(scope='session')
def make_server():
    url = b'/'

    def func(r):
        return 1

    base = BaseHandler()
    base.URLS[url] = (func, b'GET')
    return base
