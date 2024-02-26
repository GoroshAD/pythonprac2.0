from cowsay import cowsay, read_dot_cow
import sys

with open(sys.argv[1]) as f:
    cow = read_dot_cow(sys.argv[1])
    print(cowsay(sys.argv[2], sys.argv[1], cowfile=cow))
