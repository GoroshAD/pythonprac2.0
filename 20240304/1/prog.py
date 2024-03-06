from cowsay import cowsay, list_cows
import sys, shlex

field = {}
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

def encounter(x, y):
    print(cowsay(field[(x, y)].monster.phrase, cow=field[(x, y)].monster.name))

for i in range(10):
    for j in range(10):
        field[(i, j)] = Cell()
field[(0, 0)].player = True

print("<<< Welcome to Python-MUD 0.1 >>>")
player = Player()
while commands := sys.stdin.readline():
    commands = shlex.split(commands)
    length_commands = len(commands)
    match commands[0]:
        case "up":
            if length_commands > 1:
                print("Invalid arguments")
            else:
                field[(player.x, player.y)].player = False
                player.y = (player.y - 1) % 10
                field[(player.x, player.y)].player = True
                print(f"Moved to {(player.x, player.y)}")
                if field[(player.x, player.y)].monster is not None:
                    encounter(player.x, player.y)
        case "down":
            if length_commands > 1:
                print("Invalid arguments")
            else:
                field[(player.x, player.y)].player = False
                player.y = (player.y + 1) % 10
                field[(player.x, player.y)].player = True
                print(f"Moved to {(player.x, player.y)}")
                if field[(player.x, player.y)].monster is not None:
                    encounter(player.x, player.y)
        case "left":
            if length_commands > 1:
                print("Invalid arguments")
            else:
                field[(player.x, player.y)].player = False
                player.x = (player.x - 1) % 10
                field[(player.x, player.y)].player = True
                print(f"Moved to {(player.x, player.y)}")
                if field[(player.x, player.y)].monster is not None:
                    encounter(player.x, player.y)
        case "right":
            if length_commands > 1:
                print("Invalid arguments")
            else:
                field[(player.x, player.y)].player = False
                player.x = (player.x + 1) % 10
                field[(player.x, player.y)].player = True
                print(f"Moved to {(player.x, player.y)}")
                if field[(player.x, player.y)].monster is not None:
                    encounter(player.x, player.y)
        case "addmon":
            if length_commands != 9:
                print("Invalid arguments")
            else:
                name, phrase = commands[1], ""
                x, y, hp = 0, 0, 0
                try:
                    i = 2
                    while i < 9:
                        match commands[i]:
                            case "hello":
                                phrase = commands[i + 1]
                                i += 2
                            case "hp":
                                hp = commands[i + 1]
                                i += 2
                            case "coords":
                                x, y = commands[i + 1], commands[i + 2]
                                i += 3
                            case _:
                                raise ValueError
                    hp = int(hp)
                    x = int(x)
                    y = int(y)
                    if x >= 10 or x < 0 or y >= 10 or y < 0 or hp <= 0:
                        raise ValueError
                except:
                    print("Invalid arguments")
                    continue
                if name not in list_cows():
                    print("Cannot add unknown monster")
                    continue
                monster = Monster(name, x, y, phrase, hp)
                flag = True if field[(x, y)].monster is not None else False
                field[(x, y)].monster = monster
                print(f"Added monster {name} to {(x, y)} saying {phrase}")
                if flag:
                    print("Replaced the old monster")
        case _:
            print("Invalid command")


