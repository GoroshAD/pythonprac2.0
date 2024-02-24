import sys, glob, zlib
from os.path import basename, dirname

SHIFT = "   "   

def desc(store):
    with open(store, "rb") as f:
        obj = zlib.decompress(f.read())
        header, _, body = obj.partition(b'\x00')
        kind, size = header.split()
    return [header, body, kind, size]

match len(sys.argv):
    case 2:
        path = sys.argv[1]
        for i in glob.iglob(path + "/.git/refs/heads/*"):
            print(basename(i))

    case 3:
        path, branch = sys.argv[1:]
        for i in glob.iglob(path + "/.git/refs/heads/*"):
            if branch == basename(i):
                '''with open(i, "r") as f:
                    head_id = f.read().split()[0]
                for store in glob.iglob(path + "/.git/objects/??/*"):
                    if basename(dirname(store)) + basename(store) == head_id:
                        header, body, kind, size = desc(store)
                        out = body.decode().replace('\n', '\n' + SHIFT)
                        print(f"{SHIFT}{out}")
                        tree_id = out.split()[1]
                for store in glob.iglob(path + "/.git/objects/??/*"):
                    if basename(dirname(store)) + basename(store) == tree_id:
                        header, tail, kind, size = desc(store)
                        while tail:
                            treeobj, _, tail = tail.partition(b'\x00')
                            tmode, tname = treeobj.split()
                            num, tail = tail[:20], tail[20:]
                            match kind:
                                case b'tree':
                                    kind = 'tree'
                                case b'blob':
                                    kind = 'blob'
                            print(f"{SHIFT}{kind} {num.hex()} {tname.decode()}\n")'''

                commit_arr = []
                for store in glob.iglob(path + "/.git/objects/??/*"):
                    header, body, kind, size = desc(store)
                    if kind == b'commit':
                        out = body.decode().replace('\n', '\n' + SHIFT)
                        commit_arr.append((out, out.split('\n')[2].split()[3], store))
                commit_arr.sort(key = lambda x : x[1])

                for i in commit_arr:
                    print(f"TREE for commit {i[2].split('/')[-2]+i[2].split('/')[-1]}")
                    tree_id = i[0].split()[1]
                    for store in glob.iglob(path + "/.git/objects/??/*"):
                        if basename(dirname(store)) + basename(store) == tree_id:
                            header, tail, kind, size = desc(store)
                            while tail:
                                treeobj, _, tail = tail.partition(b'\x00')
                                tmode, tname = treeobj.split()
                                num, tail = tail[:20], tail[20:]
                                match kind:
                                    case b'tree':
                                        kind = 'tree'
                                    case b'blob':
                                        kind = 'blob'
                                print(f"{kind} {num.hex()} {tname.decode()}")
