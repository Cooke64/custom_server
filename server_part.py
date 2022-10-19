import enum
import functools
import socket
from re import fullmatch
from select import select
from typing import Tuple
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.FileHandler('loger_data.log'))


ERROR = {
    404: '<h1>Not found </h1>',
    405: '<h1>Method is not allowed </h1>',
}

URLS = {}


class IpAndPortError(Exception):
    pass


class UrlError(Exception):
    pass


class Nums(enum.Enum):
    AMOUNT_OF_BYTES = 1024
    LISTEN_NUMS = 4
    BAD_REQUEST = 404
    NOT_ALLOWED = 405
    STATUS_OK = 200
    MIN_PORT = 0
    MAX_PORT = 5


class Server:
    rest = 'Content-Type: text/html; charset=utf-8\r\n\r\n'
    HEADER_OK = 'HTTPS/1.1 200 OK\r\n' + rest
    BAD_REQUEST = 'HTTPS/1.1 404 Bad request\r\n' + rest
    NOT_ALLOWED = 'HTTPS/1.1 405 Method is not allowed\r\n' + rest

    to_monitor = []

    def __init__(self, url: str = 'localhost', port: int = 8000):
        if not self.check_url(url):
            raise IpAndPortError('Неправильно задан url')
        if not isinstance(
                port, int) and Nums.MIN_PORT.value < port < Nums.MAX_PORT.value:
            raise IpAndPortError('Неправильно задан port')
        self.__socket = (url, port)
        self.server = self._make_server()

    def __repr__(self):
        return self.__socket

    @staticmethod
    def check_url(value):
        regex = r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
        match = fullmatch(regex, value)
        return match or value == 'localhost'

    def _make_server(self) -> socket.socket:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.__socket)
        server.listen(Nums.LISTEN_NUMS.value)
        return server

    def _make_con(self, server: socket.socket) -> None:
        client_side, _ = server.accept()
        self.to_monitor.append(client_side)

    def _make_headers(self, method: bytes, url: bytes) -> Tuple[str, int]:
        if not method == b'GET':
            log.info(f'The method {method} is prohibited')
            return self.NOT_ALLOWED, Nums.NOT_ALLOWED.value
        if url not in URLS:
            log.info(f'There`s no page with url {url}')
            return self.BAD_REQUEST, Nums.BAD_REQUEST.value
        return self.HEADER_OK, Nums.STATUS_OK.value

    @staticmethod
    def _get_view(code: int, url: str):
        if code in [Nums.NOT_ALLOWED.value, Nums.BAD_REQUEST.value]:
            return ERROR[code]
        return URLS[url][0]()

    def _generate_response(self, request: bytes) -> bytes:
        """Генерирует ответ сервер. в виде ответа пользователю и headers"""
        method, url, *_ = request.split()
        headers, code = self._make_headers(method, url)
        view = self._get_view(code, url)
        return (headers + view).encode('utf-8')

    def _send_message(self, client_side) -> None:
        request = client_side.recv(Nums.AMOUNT_OF_BYTES.value)
        if request:
            response = self._generate_response(request)
            client_side.send(response)
        else:
            client_side.close()

    def run_server(self) -> None:
        self.to_monitor.append(self.server)
        while True:
            try:
                ready_to_read, _, _ = select(self.to_monitor, [], [])

                for sock in ready_to_read:
                    if sock is self.server:
                        self._make_con(sock)
                    else:
                        self._send_message(sock)

            except ValueError:
                self.to_monitor.pop()


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
    return '<h1>Hey, bud</h1><br><a href="http://127.0.0.1:7777/blog/">Look at my blog page</a>'


@router(url=b'/blog')
def blog():
    return '<h1>Hello, world and look at my code!</h1>'


if __name__ == '__main__':
    s = Server('127.0.0.1', 7777)
    s.run_server()
