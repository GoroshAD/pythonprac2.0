import sys, glob, zlib
from os.path import basename, dirname

SHIFT = "   "   

match len(sys.argv):
    case 2:
        path = sys.argv[1]
        for i in glob.iglob(path + "/.git/refs/heads/*"):
            print(basename(i))

    case 3:
        path, branch = sys.argv[1:]
        for i in glob.iglob(path + "/.git/refs/heads/*"):
            if branch == basename(i):
                with open(i, "r") as f:
                    head_id = f.read().split()[0]
                for store in glob.iglob(path + "/.git/objects/??/*"):
                    if basename(dirname(store)) + basename(store) == head_id:
                        with open(store, "rb") as f:
                            obj = zlib.decompress(f.read())
                            header, _, body = obj.partition(b'\x00')
                            kind, size = header.split()
                            out = body.decode().replace('\n', '\n' + SHIFT)
                            print(f"{SHIFT}{out}")


