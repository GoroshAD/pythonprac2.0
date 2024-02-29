from cowsay import cowsay
import sys

field = {}
class Monster:
    phrase = ""
    def __init__(self, phrase):
        self.phrase = phrase

class Player:
    x = 0
    y = 0

class Cell:
    monster = None
    player = False

def encounter(x, y):
    print(cowsay(f"{field[(x, y)].monster.phrase}"))

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
            if length_commands != 4:
                print("Invalid arguments")
            else:
                monster = Monster(commands[3])
                try:
                    commands[1] = int(commands[1]) % 10
                    commands[2] = int(commands[2]) % 10
                except:
                    print("Invalid arguments")
                    continue
                flag = True if field[(commands[1], commands[2])].monster is not None else False
                field[(commands[1], commands[2])].monster = monster
                print(f"Added monster to {(commands[1], commands[2])} saying {monster.phrase}")
                if flag:
                    print("Replaced the old monster")
        case _:
            print("Invalid command")


