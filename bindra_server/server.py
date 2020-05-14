from aiohttp import web
import logging
import sys
import subprocess
import asyncio
import json

class BindraServer():
    """
    Ghidra socket.io server
    """

    async def ghrequest(self, message):
        reader, writer = await asyncio.open_connection(
                '127.0.0.1',
                6666
                )
        writer.write(message.encode('utf8'))
        writer.write_eof()
        await writer.drain()
        request = b''
        while True:
            tp = await reader.read(1024)
            request += tp
            reader.feed_eof()
            if reader.at_eof():
                break
        print(request.decode('utf8'))
        writer.close()
        await writer.wait_closed()
        return request

    def __init__(self):
        """
        Initialize the Bindra Socket.IO server

        @params port The port to run the server on
        """
        self._app = web.Application()
        self.__init_routes()
        print('Initialized bindra server.')

    def __handle_index(self, request):
        return web.Response(text='This is the index. If you see this you are using me wrong!')

    def __handle_status(self, request):
        print(dir(ghidra))

    async def __handle_test(self, request):
        response = await self.ghrequest(json.dumps({
                "request": "getCurrentProgram",
                "args": [
                ]
            }))
        print('Got response: ', response)
        return web.Response(text=response.decode('utf8'))

    def __init_routes(self):
        self._app.router.add_get(
                '/', 
                self.__handle_index
                )

        self._app.router.add_post(
                '/status', 
                self.__handle_status
                )

        self._app.router.add_get(
                '/test',
                self.__handle_test
                )

    def run(self):
        web.run_app(self._app)


if __name__ == "__main__":
    print('Starting bindra server.')
    bs = BindraServer()
    bs.run()
    print('Started bindra server.')


