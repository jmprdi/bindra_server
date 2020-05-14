import socket
import json
import subprocess
import os
import ghidra

"""
This server is run by Ghidra's Jython 2.7

It handles requests from the main Bindra server
and returns to the Bindra server the requested data
or performs the requested actions.
"""

HOST, PORT = "localhost", 6666


def get_current_program(args):
    """
    Test function to make sure we're running right
    """
    print('got current program {}'.format(currentProgram))
    return currentProgram
    
handlers = {
        'getCurrentProgram': get_current_program
}

def handle(request):
    try:
        request = json.loads(request)
    except JSONDecodeError as e:
        print('Error: request {} was not valid json.'.format(request))

    response = {
            'type': request['type'],
            'data': handlers[request['type']](request['args']),
            'stamp': stamp
        }
    stamp += 1
    return json.dumps(response)

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    while True:
        connection, client = sock.accept()
        request = b''
        try:
            while True:
                data = connection.recv(1024)
                if data:
                    request += data
                else:
                    break
            response = handle(request)
            connection.sendall(response)
        except Exception as e:
            print('Connection exception with {}: {}'.format(client, e))
        finally:
            connection.close()

def start_bindra():
    with open('/tmp/script.log', 'wb') as out:
        return subprocess.Popen(['python3', os.path.join('/tmp/bindra_server/bindra_server', 'server.py')], stdout=out, stderr=out)

if __name__ == "__main__":
    try:
        print('Initializing bindra server.')
        bs = start_bindra()
        start_server()
    except KeyboardInterrupt:
        bs.kill()
    except Exception as e:
        print('Fatal error. Exiting.')
        print(e)


