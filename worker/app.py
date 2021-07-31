import logging
from socketserver import TCPServer

from worker.handler import Handler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    with TCPServer(("0.0.0.0", 3130), Handler) as server:
        server.serve_forever()
