import enum
import functools

from custom_server.custom_exception import UrlError
from custom_server.server_part import URLS


def check_decorator(url):
    if not url.decode().startswith('/'):
        raise UrlError('Ссылка должна начинаться с символа "/"')
    elif url in URLS:
        raise UrlError('Такой адрес уже есть')


def router(url, method=b'GET'):
    def decorator(func):
        try:
            check_decorator(url)
            URLS[url] = (func, method)
        except:
            raise

        @functools.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return decorator
