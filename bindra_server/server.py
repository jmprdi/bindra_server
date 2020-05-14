from aiohttp import web
import logging

#import ghidra

class BindraServer():
    """
    Ghidra socket.io server
    """

    def __init__(self):
        """
        Initialize the Bindra Socket.IO server

        @params port The port to run the server on
        """
        self._app = web.Application()
        self.__init_routes()
        self._port = port
        print('Initialized bindra server.')

    def __handle_index(self, request):
        print('got request')

    def __handle_status(self, request):
        print(dir(ghidra))


    def __init_routes(self):
        self._app.router.add_get(
                '/', 
                self.__handle_index
                )

        self._app.router.add_post(
                '/status', 
                self.__handle_status
                )


    def run(self):
        web.run_app(self._app)

if __name__ == "__main__":
    print('Starting bindra server.')
    bs = BindraServer()
    bs.run()
    print('Started bindra server.')


