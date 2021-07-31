from logging import getLogger
from socket import socket
from socketserver import BaseRequestHandler

from worker.database import lookup

logger = getLogger(__name__)


def transform(message: str) -> str:
    return ", ".join(lookup(message, 3))


class Handler(BaseRequestHandler):
    buf_size = 2048
    encoding = "UTF-8"

    def handle(self) -> None:
        self.request: socket

        incoming_data = self.request.recv(self.buf_size).decode(self.encoding).strip()
        logger.info(f'Incoming data = """{incoming_data}"""')

        outgoing_data = transform(incoming_data)
        logger.info(f'Outgoing data = """{outgoing_data}"""')

        self.request.sendall(outgoing_data.encode(self.encoding))
