from cowsay import cowsay, list_cows
import sys

field = {}
class Monster:
    name = ""
    x = 0
    y = 0
    phrase = ""
    def __init__(self, name, x, y, phrase):
        self.phrase = phrase
        self.x = x
        self.y = y
        self.name = name

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

player = Player()
while commands := sys.stdin.readline():
    commands = commands.split()
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
            if length_commands != 5:
                print("Invalid arguments")
            else:
                name = commands[1]
                x = commands[2]
                y = commands[3]
                phrase = commands[4]
                try:
                    x = int(x)
                    y = int(y)
                    if x >= 10 or x < 0 or y >= 10 or y < 0:
                        raise ValueError
                except:
                    print("Invalid arguments")
                    continue
                if name not in list_cows():
                    print("Cannot add unknown monster")
                    continue
                monster = Monster(name, x, y, phrase)
                flag = True if field[(x, y)].monster is not None else False
                field[(x, y)].monster = monster
                print(f"Added monster {name} to {(x, y)} saying {phrase}")
                if flag:
                    print("Replaced the old monster")
        case _:
            print("Invalid command")


