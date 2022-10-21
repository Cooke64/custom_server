import enum
import functools
import json
import logging
from typing import Tuple, Union, Any

from custom_exception import UrlError
from src.make_user_socket import UserSocket

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler('loger_data.log'))

URLS = {}


class Nums(enum.Enum):
    BAD_REQUEST = 404
    NOT_ALLOWED = 405
    STATUS_OK = 200


class WorkServer(UserSocket):
    _rest = 'Content-Type: text/html; charset=utf-8\r\n\r\n'
    _HEADER_OK = 'HTTPS/1.1 200 OK\r\n' + _rest
    _BAD_REQUEST = 'HTTPS/1.1 404 Bad request\r\n' + _rest
    _NOT_ALLOWED = 'HTTPS/1.1 405 Method is not allowed\r\n' + _rest

    _ERROR = {
        404: '<h1>Not found </h1>',
        405: '<h1>Method is not allowed </h1>',
    }

    def __init__(self, url: str = 'localhost', port: int = 8000,
                 debug: bool = False):
        super().__init__(url, port)
        self.debug = debug

    def _make_headers(self, method: bytes, url: bytes) -> Tuple[str, int]:
        """
        :param method: принимает вид метода, с которым пользователь сделал запрос.
        :param url: принимает url, по которому обращается пользователь.
        :return: Возвращает заголовок и статус код ответа сервера.
        """
        if not method == b'GET':
            log.info(f'The method {method} is prohibited')
            return self._NOT_ALLOWED, Nums.NOT_ALLOWED.value
        if url not in URLS:
            log.info(f'There`s no page with url {url}')
            return self._BAD_REQUEST, Nums.BAD_REQUEST.value
        return self._HEADER_OK, Nums.STATUS_OK.value

    def _get_view(self, code: int, url: str) -> Union[Any]:
        if code in [Nums.NOT_ALLOWED.value, Nums.BAD_REQUEST.value]:
            return self._ERROR[code]
        return URLS[url][0]()

    def _generate_response(self, request: bytes) -> bytes:
        """Генерирует ответ сервер. в виде ответа пользователю и headers"""
        method, url, *_ = request.split()
        headers, code = self._make_headers(method, url)
        view = self._get_view(code, url)
        return (headers + view).encode('utf-8')

    def _debug_response(self, request: bytes):
        """При включенном атрибуте debug возвращает параметры запроса"""
        # генератор создает ответ, который разделяется между собой переносом строки
        url = (
            str(i) + '<br>' for i in request.split(b'\r\n') if i
        )
        # создает заголовок, с соединенным ответом
        return (self._HEADER_OK + ''.join(url)).encode('utf-8')

    def send_request(self, request) -> None:
        return (
            self._generate_response(request),
            self._debug_response(request)
        )[self.debug]


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


@router(url=b'/')
def index():
    some_data = {'first': '<a href=/blog>link</a>',
                 'second': '<a href=/second>link</a>'}
    return json.dumps(some_data)


@router(url=b'/blog')
def blog():
    return '<h1>Hello, world and look at my code!</h1>'


@router(url=b'/second')
def blog():
    return '<h1>It`s a second page</h1>'
