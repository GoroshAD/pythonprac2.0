import sys
import socket
import cmd

class Comms(cmd.Cmd):
    """
    comms
    """
    prompt = ":"
    s = 0

    def __init__(self, s):
        super().__init__()
        self.s = s

    def do_info(self, args):
        self.s.sendall((" ".join(["info", args])).encode())
        print(self.s.recv(1024).rstrip().decode())

    def complete_info(self, text, line, begidx, endidx):
        return [c for c in ["host", "port"] if c.startswith(text)]

    def do_print(self, args):
        self.s.sendall(" ".join(["print", args]).encode())
        print(self.s.recv(1024).rstrip().decode())

if __name__ == "__main__":
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        Comms(s).cmdloop()
