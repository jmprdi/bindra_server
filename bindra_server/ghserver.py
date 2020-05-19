import logging
import sys
import SocketServer
import socket
import json
import subprocess
import os

import ghidra


logging.basicConfig(level=logging.DEBUG,
        format='%(name)s: %(message)s',
        )

def handler_test(args):
    return currentProgram.__repr__()

def handler_functions(args):
    program = currentProgram
    functions = program.getFunctionManager().getFunctions(True)
    response = [{'name': f.getName(), 'address': int('0x'+ f.getEntryPoint().__repr__(), 16)} for f in functions]
    return response

    #return 'TEST_RESPONSE'

def handler_decompile(args):
    addr = int(args[0])
    address = ghidra.program.model.address.GenericAddress().getAddress(str(hex(addr)))
    program = currentProgram
    function = program.getFunctionManager().getFunctionAt(address)
    decomp = ghidra.app.decompiler.DecompInterface().decompileFunction(function, 0, ghidra.util.task.ConsoleTaskMonitor())
    response = decomp.getDecompiledFunction.getC()
    return response

handlers = {
        'test': handler_test,
        'functions': handler_functions,
        'decompile': handler_decompile
        }

def process(request, logger):
    """
    Processes a request from the web server and returns the correct response

    @param request A raw request from the web server
    @param logger The request handler's logger
    """

    json_request = json.loads(request)
    logger.debug('Processing request {}'.format(json_request))
    response = handlers[json_request['request']](json_request['args'])
    return json.dumps(response)

class GhidraRequestHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        """
        Initializes a handler to respond to an incoming address

        @param request Handle to incoming connection
        @param client_address Tuple defining address/port pair for the server
        @param server The server instance 
        """

        self.logger = logging.getLogger('GhidraServer')
        self.logger.debug('Initialized Ghidra Request Handler.')
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def handle(self):
        """
        Handles incoming requests and sends responses
        """

        self.logger.debug('Handling request from {}'.format(self.client_address))
        rsize = b''
        while True:
            data = self.request.recv(1)
            if not data or data == b'\n':
                break
            rsize += data
        rsize = int(rsize)
        self.logger.debug('Request size {}'.format(rsize))
        request = self.request.recv(rsize)
        self.logger.debug('Request contents {}'.format(request))
        response = process(request, self.logger)

        self.request.send(response)
        return

class GhidraServer(SocketServer.TCPServer):
    """
    GhidraServer is a TCP socket server that receives a request from the web
    API server, grabs information from Ghidra, and returns it to the server
    """

    def __init__(self, server_address, handler_class=GhidraRequestHandler):
        """
        TCP Server initializer

        @param server_address Defines the address/port pair for the server
        @param handler_class Subclass of BaseRequestHandler that handles incoming requests
        """

        self.logger = logging.getLogger('GhidraServer')
        self.logger.debug('Initialized Ghidra Server')
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

def startp3server():
    return subprocess.Popen(['python3', '/tmp/bindra_server/bindra_server/server.py'])

if __name__ == '__main__':
    startp3server()
    address = ('localhost', 6666) # let the kernel give us a port
    server = GhidraServer(address, GhidraRequestHandler)
    ip, port = server.server_address # find out what port we were given
    server.serve_forever()

