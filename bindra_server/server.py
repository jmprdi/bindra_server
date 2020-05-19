from aiohttp import web
import socket
import logging
import sys
import subprocess
import asyncio
import json

# import ghidra

HOST = 'localhost'
PORT = 6666


class BindraServer():
    def __init__(self):
        self._app = web.Application()
        self._app.router.add_get(
                '/',
                self.request
                )

    def test_request(self):
        request = {
                'request': 'test',
                'args': []
        }
        request = bytes(json.dumps(request), 'utf8')
        return request

    def run(self):
        web.run_app(self._app)

    def request(self, _request):
        """
        Responds to a request from the Binara Binary Ninja plugin
        Requests the correct data from the ghserver, gets the result, and
        sends it back to Binary Ninja

        Note: This is a client
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        # Needs bytes
        sock.send(bytes(str(len(self.test_request())), 'utf8') + b'\n')
        sock.send(self.test_request())
        response = b''
        try:
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                response += data
        except Exception as e:
            print('error', e)
        finally:
            print('Received ', repr(response))
            sock.close()
        return web.Response(text=response.decode('utf8'))

if __name__ == "__main__":
    bs = BindraServer()
    bs.run()
