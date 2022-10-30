import enum
import functools
import logging
from re import fullmatch, search
from typing import Tuple, Union, Any

from custom_exception import UrlError
from src.make_user_socket import UserSocket
from src.response_data import Response

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler('loger_data.log'))


class Nums(enum.Enum):
    BAD_REQUEST = 404
    NOT_ALLOWED = 405
    STATUS_OK = 200


class BaseHandler(UserSocket):
    _rest = 'Content-Type: text/html; charset=utf-8\r\n\r\n'
    _HEADER_OK = 'HTTPS/1.1\r\n' + _rest
    _BAD_REQUEST = 'HTTPS/1.1 404 Bad request\r\n' + _rest
    _NOT_ALLOWED = 'HTTPS/1.1 405 Method is not allowed\r\n' + _rest

    _ERROR = {
        404: '<h1>Not found </h1>',
        405: '<h1>Method is not allowed </h1>',
    }

    URLS = {}
    SLUG_URLS = {}

    def __init__(self, url: str = '127.0.0.1', port: int = 7777,
                 debug: bool = False):
        super().__init__(url, port)
        self.debug = debug

    def __call__(self, *args, **kwargs):
        return self.run_server()

    def _get_slug(self, url: bytes):
        _, *slug_data, _ = url.split(b'/')
        return tuple(slug_data)

    def _make_headers(self, method: bytes, url: bytes) -> Tuple[str, int]:
        """
        :param method: принимает вид метода, с которым пользователь сделал запрос.
        :param url: принимает url, по которому обращается пользователь.
        :return: Возвращает заголовок и статус код ответа сервера.
        """
        bool_value = url not in self.URLS and self._get_slug(url) not in self.SLUG_URLS
        if bool_value:
            log.info(f'There`s no page with url {url}')
            return self._BAD_REQUEST, Nums.BAD_REQUEST.value
        match method:
            case b'GET':
                return self._HEADER_OK, Nums.STATUS_OK.value
            case _:
                log.info(f'The method {method} is prohibited')
                return self._NOT_ALLOWED, Nums.NOT_ALLOWED.value

    def _get_view(self, code: int, url: bytes, response: bytes) -> Union[Any]:
        """
        Функция обработчик отображения ответа пользователю
        при запросе на определенный адрес.
        :param code: код ответа сервера.
        :param url: адрес, по которому был сделан запрос.
        :param response: передается ответ сервера, представленный в байтах.
        :return: вызов функции, в зависимости от переданного url и кода ответа.
        """
        match code:
            case Nums.STATUS_OK.value:
                # Вызов функции из словаря, где ключ это адрес страницы, а значение
                # это вью функция отображения. Передается объект класса Response
                try:
                    return self.URLS[url][0](Response(response))
                except KeyError:
                    return self.SLUG_URLS[self._get_slug(url)][0](Response(response))
            case Nums.NOT_ALLOWED.value | Nums.BAD_REQUEST.value:
                return self._ERROR[code]
            case _:
                raise ValueError('Нет такого кода для обработки.')

    def _generate_response(self, response: bytes) -> bytes:
        """Генерирует ответ сервер. в виде ответа пользователю и headers"""
        method, url, *_ = response.split()
        headers, code = self._make_headers(method, url)
        view = self._get_view(code, url, response=response)
        if isinstance(view, tuple):
            return (headers + view[0]).encode('utf-8')
        return (headers + view).encode('utf-8')

    def _debug_response(self, request: bytes):
        """При включенном атрибуте debug возвращает параметры запроса"""
        # генератор создает ответ, который разделяется между собой переносом строки
        url = (
            str(i) + '<br>' for i in request.split(b'\r\n') if i
        )
        # создает заголовок, с соединенным ответом
        return (self._HEADER_OK + ''.join(url)).encode('utf-8')

    def _send_request(self, request: bytes) -> None:
        return (
            self._generate_response(request),
            self._debug_response(request)
        )[self.debug]


class Router(BaseHandler):
    def check_decorator(self, url):
        if not url.decode().startswith('/'):
            raise UrlError('Ссылка должна начинаться с символа "/"')
        elif url in self.URLS:
            raise UrlError('Такой адрес уже есть')
        return True

    def get_slug(self, url: bytes) -> str | None:
        # Сделать декомпозицию этой функции, поймать исключения, моменты, гдн может упасть
        regex = r'.+/<.+>'
        regex_slug = r'<.+>'
        url = url.decode()
        if fullmatch(regex, url):
            return search(regex_slug, url).group().replace('<', '').replace('>', '')

    def view_router(self, url, method=b'GET'):
        def decorator(func):
            try:
                if self.check_decorator(url):
                    slug = self.get_slug(url)
                    if slug:
                        link = url.split(b'/')[1]
                        self.SLUG_URLS[(link, slug.encode('utf-8'))] = (func, method)
                    self.URLS[url] = (func, method)
            except UrlError:
                raise

            @functools.wraps(func)
            def inner(*args, **kwargs):
                data = func(*args, **kwargs)
                return data

            return inner

        return decorator
