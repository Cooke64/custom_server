import socket
from select import select

from src.make_server import Server


class UserSocket(Server):
    def __init__(self, url, port):
        super().__init__(url, port)

    __TO_MONITOR = []

    def _make_con(self, server_socket: socket.socket) -> None:
        client_side, _ = server_socket.accept()
        self.__TO_MONITOR.append(client_side)

    def _send_message(self, client_side) -> None:
        request = client_side.recv(4048)
        if request:
            response = self.send_request(request)
            client_side.send(response)
        else:
            client_side.close()

    def send_request(self, request) -> None:
        raise NotImplementedError

    def run_server(self) -> None:
        self.__TO_MONITOR.append(self.server)
        while True:
            try:
                ready_to_read, _, _ = select(self.__TO_MONITOR, [], [])

                for sock in ready_to_read:
                    if sock is self.server:
                        self._make_con(sock)
                    else:
                        self._send_message(sock)

            except ValueError:
                self.__TO_MONITOR.pop()
