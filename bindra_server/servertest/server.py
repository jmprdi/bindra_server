import socket

HOST = ''
PORT = 50007 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)


while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    request = b''
    try:
        while True:
            data = conn.recv(1024)
            if not data: 
                break
            request += data
    except:
        print('error')
    finally:
        print('Got ', request)
        conn.sendall(b'ok')
        conn.shutdown(socket.SHUT_WR)
        conn.close()
