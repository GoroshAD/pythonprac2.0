import multiprocessing, shlex, sys, socket

#Constants and dictionaries.

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
field = {}

#Necessary classes.

class Monster:
    name = ""
    x = 0
    y = 0
    phrase = ""
    hp = 0
    def __init__(self, name, x, y, phrase, hp):
        self.phrase = phrase
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp

class Player:
    x = 0
    y = 0

class Cell:
    monster = None
    player = False

#Loading game map.

for i in range(10):
    for j in range(10):
        field[(i, j)] = Cell()
field[(0, 0)].player = True
player = Player()

#Game functions.

def serve(conn, addr):
    with conn:
        print('Connected by', addr)
        while data := conn.recv(1024):
            inf = shlex.split(data.decode())
            match inf[0]:
                case "move":
                    field[(player.x, player.y)].player = False
                    player.x = (player.x + inf[1]) % 10
                    player.y = (player.y + inf[2]) % 10
                    field[(player.x, player.y)].player = True
                    monster_name, monster_phrase = None, None
                    if field[(player.x, player.y)].monster is not None:
                        monster_name = field[(player.x, player.y)].monster.name
                        monster_phrase = field[(player.x, player.y)].monster.phrase
                    conn.sendall(f"{player.x} {player.y} {monster_name} {monster_phrase}").encode())
                case "addmon":
                    name, x, y, phrase, hp = inf[1:]
                    monster = Monster(name, x, y, phrase, hp)
                    replaced_monster_flag = True if field[(x, y)].monster is not None else False
                    field[(x, y)].monster = monster
                    conn.sendall((f"{replaced_monster_flag}").encode())
                case "attack":
                    if field[(player.x, player.y)].monster is None or \
                            field[(player.x, player.y)].monster.name != inf[1]:
                        conn.sendall((f"{False}").encode())
                    else:
                        damage = inf[2]
                        if field[(player.x, player.y)].monster.hp > damage:
                            field[(player.x, player.y)].monster.hp -= damage
                            conn.sendall((f"{True} {damage} {field[(player.x, player.y)].monster.hp}").encode())
                        else:
                            damage = field[(player.x, player.y)].monster.hp
                            field[(player.x, player.y)].monster = None
                            conn.sendall((f"{True} {damage} {0}").encode())
                case _:
                    pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    while True:
        conn, addr = s.accept()
        multiprocessing.Process(target=serve, args=(conn, addr)).start()
    s.close()
