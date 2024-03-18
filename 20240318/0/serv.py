import socket
import sys
import multiprocessing
import shlex

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])

def serve(conn, addr):
    with conn:
        print('Connected by', addr)
        while data := conn.recv(1024):
            inf = shlex.split(data.decode())
            match inf[0]:
                case "print":
                    conn.sendall(shlex.join(inf[1:]).encode())
                case "info":
                    conn.sendall(str(addr[0]).encode() if inf[1] == "host" else str(addr[1]).encode())
                case _:
                    pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    while True:
        conn, addr = s.accept()
        multiprocessing.Process(target=serve, args=(conn, addr)).start()
    s.close()
