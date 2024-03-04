import shlex
try:
    print(shlex.join(shlex.split(input())))
except Exception as E:
    print(E)
