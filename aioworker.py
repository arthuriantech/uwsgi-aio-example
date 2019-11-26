import asyncio
import uvloop

loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)

import socket
import signal
import logging
import uwsgi

from aiohttp.web import AppRunner
from aiohttp.web import SockSite


async def main(app, sock):
    runner = AppRunner(app)
    await runner.setup()
    site = SockSite(runner, sock, shutdown_timeout=3)
    await site.start()


def destroy():
    print(f'destroy worker {uwsgi.worker_id()}')
    loop.stop()


if __name__ == '__main__':
    from server import app
    from server import routes

    logging.basicConfig(level=logging.DEBUG)
    app.add_routes(routes)

    loop.add_signal_handler(signal.SIGINT, destroy)
    loop.add_signal_handler(signal.SIGHUP, destroy)

    for fd in uwsgi.sockets:
        sock = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
        loop.create_task(main(app, sock))

    try:
        uwsgi.accepting()
        loop.run_forever()
    finally:
        loop.close()

