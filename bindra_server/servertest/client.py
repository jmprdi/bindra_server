import socket

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'Hello, world')
s.shutdown(socket.SHUT_WR)
try:
    data = b''
    while True:
        buf = s.recv(1024)
        if not buf:
            break
        data += buf
except:
    print('error')
finally:
    print('Received', repr(data))
    s.close()
