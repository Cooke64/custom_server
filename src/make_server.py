import enum
import socket

from src.services import check_params


class Value(enum.Enum):
    LISTEN_NUMS = 4
    MIN_PORT = 0
    MAX_PORT = 65535


class Server:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not Server.__instance:
            Server.__instance = super(Server, cls).__new__(
                cls, *args, **kwargs
            )
        return Server.__instance

    def __init__(self, url: str, port: int):
        if check_params(url, port):
            self.__socket = (url, port)
            self.server = self.__make_server()

    def __make_server(self) -> socket.socket:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.__socket)
        server_socket.listen(Value.LISTEN_NUMS.value)
        return server_socket
