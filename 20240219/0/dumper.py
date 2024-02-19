import sys, zlib

with open(sys.argv[1], "rb") as f:
    compress = f.read()
print(zlib.decompress(compress))
