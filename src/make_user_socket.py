import socket
from select import select

from src.make_server import Server


class UserSocket(Server):
    __TO_MONITOR = []

    def _make_con(self, server_socket: socket.socket) -> None:
        client_side, _ = server_socket.accept()
        self.__TO_MONITOR.append(client_side)

    def _send_message(self, client_side: socket.socket) -> None:
        response = client_side.recv(4048)

        if response:
            response = self._send_response(response)
            client_side.send(response)
        else:
            client_side.close()

    def _send_response(self, response) -> None:
        raise NotImplementedError(
            'Необходимо переопределить этот метод в дочернем классе'
        )

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
