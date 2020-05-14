import socket
import json
import subprocess
import os
# import ghidra

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
    return currentProgram.encode('utf8')

def test(args):
    print('GOT TEST')
    return 'TEST SUCCESSFUL'

handlers = {
        'getCurrentProgram': get_current_program,
        'test': test
        }

def handle(request):
    print('handling request: ', request, type(request))
    try:
        request = json.loads(request)
    except Exception as e:
        print('Error: request {} was not valid json.'.format(request))

    print('Got request: ', request)

    try:
        data = handlers[request['request']](request['args'])
    except Exception as e:
        print('Error in handler', e)

    response = {
            'type': request['request'],
            'data': data,
            }
    try:
        response = bytes(json.dumps(response), 'utf8')
    except Exception as e:
        print('dump error ', e)
    print('Responding with: ', response)
    return response

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    while True:
        connection, client = sock.accept()
        print('Got connection')
        request = b''
        try:
            while True:
                data = connection.recv(1024)
                if data:
                    request += data
                else:
                    break
            print('Request: ', request)
            response = handle(request)
            print('Sending response: ', response, type(response))
            connection.sendall(response)
        except Exception as e:
            print('Connection exception with {}: {}'.format(client, e))
            connection.sendall('ERROR' + str(e))
        finally:
            connection.close()

def start_bindra():
    with open('/tmp/script.log', 'ab') as out:
        return subprocess.Popen(['python3', os.path.join('/tmp/bindra_server/bindra_server', 'server.py')], stdout=out, stderr=out)
    #return subprocess.Popen(['python3', os.path.join('.', 'server.py')])
    #pass

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
