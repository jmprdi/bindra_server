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

HOST, PORT = '', 6666


def get_current_program(args):
    """
    Test function to make sure we're running right
    print('got current program {}'.format(currentProgram))
    return str(currentProgram)
    """
    return "bash"

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
    print('Response is: ', response)
    try:
        response = json.dumps(response)
    except Exception as e:
        print('dump error ', e)
    print('Responding with: ', response)
    return response

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        print('Connection from ', addr)
        request = b''
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                request += data
        except:
            print('Error in start_server')
        finally:
            response = request #handle(request)
            print('Sending ', response)
            conn.sendall(response)
            conn.shutdown(socket.SHUT_WR)
            conn.close()

def start_bindra():
    """
    with open('/tmp/script.log', 'ab') as out:
        return subprocess.Popen(['python3', os.path.join('/tmp/bindra_server/bindra_server', 'server.py')], stdout=out, stderr=out)
    """
    return subprocess.Popen(['python3', os.path.join('.', 'server.py'), './script.log'])
    #pass

if __name__ == "__main__":
    try:
        print('Initializing bindra server.')
        #bs = start_bindra()
        print('Initialized bindra server')
        start_server()
    except KeyboardInterrupt:
        #bs.kill()
        pass
    except Exception as e:
        print('Fatal error. Exiting.')
        #bs.kill()
        print(e)
