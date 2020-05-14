import socket
import asyncio
import json
import subprocess
import os

"""
This server is run by Ghidra's Jython 2.7

It handles requests from the main Bindra server
and returns to the Bindra server the requested data
or performs the requested actions.
"""

HOST, PORT = "localhost", 6666

async def handle(reader, writer):
    print('Got request: ')
    request = b''
    while True:
        tp = await reader.read(1024)
        request += tp
        reader.feed_eof()
        if reader.at_eof():
            break
    request = json.loads(request)
    print('Got request: ', request)
    writer.write(b'OK')
    await writer.drain()
    print('Closing channel.')
    writer.close()
    await writer.wait_closed()

def start_bindra():
    return subprocess.Popen(['python3', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'server.py')])

if __name__ == "__main__":
    try:
        print('Initializing bindra server.')
        bs = start_bindra()
        print('Starting bindra->ghidra bridge server.')
        loop = asyncio.get_event_loop()
        loop.create_task(asyncio.start_server(handle, HOST, PORT))
        loop.run_forever()
        print('Closed bindra->ghidra bridge server.')
    except KeyboardInterrupt:
        bs.kill()


