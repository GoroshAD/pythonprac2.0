from http import server
import sys
import socket

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
s.close()
server.test(HandlerClass=server.SimpleHTTPRequestHandler, port=int(sys.argv[1]))
