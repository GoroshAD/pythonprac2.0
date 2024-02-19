import glob, zlib, sys

PATH = sys.argv[1]
for i in glob.iglob(PATH + "/??/*"):
    with open(i, "rb") as f:
        content = zlib.decompress(f.read())
    match content.partition(b' ')[0]:
        case b'commit':
            print(content.partition(b'\x00')[2].decode())
        case b'tree':
            



