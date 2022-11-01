import enum
import socket
from re import fullmatch

from custom_exception import IpAndPortError


class Value(enum.Enum):
    LISTEN_NUMS = 4
    MIN_PORT = 0
    MAX_PORT = 65535


class Server:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Server.__instance:
            Server.__instance = super(Server, cls).__new__(cls, *args, **kwargs)
        return Server.__instance

    def __init__(self, url: str, port: int):
        if self.__check_params(url, port):
            self.__socket = (url, port)
            self.server = self.__make_server()

    def __check_params(self, url: str, port: int) -> bool | None:
        if not self.validate_url(url):
            raise IpAndPortError('Неправильно задан url')
        check_value = Value.MIN_PORT.value < port <= Value.MAX_PORT.value
        if not isinstance(port, int) | check_value:
            raise IpAndPortError('Неправильно задан port')
        else:
            return True

    @staticmethod
    def validate_url(value: str) -> bool:
        """Проверяет соответствие переданного ip адреса установленным правилам написания ip"""
        regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        match = fullmatch(regex, value)
        return match or value == 'localhost'

    def __make_server(self) -> socket.socket:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.__socket)
        server_socket.listen(Value.LISTEN_NUMS.value)
        return server_socket
