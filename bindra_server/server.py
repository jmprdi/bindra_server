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
                self.send_request
                )
        self.requesters = {
                'test': self.request_test,
                'functions': self.request_functions,
                'decompile': self.request_decompile
                }

    def request_test(self, args):
        """
        Requests a test from the ghserver

        @param args Unused
        @returns JSON-ified bytes request
        """
        request = {
                'request': 'test',
                'args': []
                }
        request = bytes(json.dumps(request), 'utf8')
        return request

    def request_functions(self, args):
        """
        Requests a list of functions from the ghserver

        @param args Unused
        @returns JSON-ified bytes request
        """
        request = {
                'request': 'functions',
                'args': []
                }
        request = bytes(json.dumps(request), 'utf8')
        return request

    def request_decompile(self, args):
        """

        """
        request = {
                'request': 'decompile',
                'args': [
                    int(args.split(',')[0])
                    ]
                }
        request = bytes(json.dumps(request), 'utf8')
        return request

    def run(self):
        web.run_app(self._app)

    def send_request(self, _request):
        """
        Responds to a request from the Binara Binary Ninja plugin
        Requests the correct data from the ghserver, gets the result, and
        sends it back to Binary Ninja

        Note: This is a client
        """

        query = _request.query
        request = self.requesters[query['type']](query['args'])

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        # Needs bytes
        sock.send(bytes(str(len(request)), 'utf8') + b'\n')
        sock.send(request)
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
