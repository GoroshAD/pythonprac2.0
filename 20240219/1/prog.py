import sys, glob

match len(sys.argv):
    case 2:
        path = sys.argv[1]
        for i in glob.iglob(path + "/.git/refs/heads/*"):
            print(i[i.rfind("/") + 1:])
