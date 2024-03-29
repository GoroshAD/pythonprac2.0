from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO
import sys, shlex, cmd

#Necessary classes, dictionaries etc.

JGSBAT = StringIO("""$the_cow = <<EOC;
   $thoughts
    $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.| \\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __ \\'--'//__
         (((""`  `"")))
EOC""")

field = {}
weapons ={"sword": 10, "spear": 15, "axe": 20}

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

def encounter(x, y):
    if field[(x, y)].monster.name == "jgsbat":
        print(cowsay(field[(x, y)].monster.phrase, cowfile=read_dot_cow(JGSBAT)))
    else:
        print(cowsay(field[(x, y)].monster.phrase, cow=field[(x, y)].monster.name))
    return

def up_func(args):
    if len(shlex.split(args)) > 0:
        print("Invalid arguments")
        return
    field[(player.x, player.y)].player = False
    player.y = (player.y - 1) % 10
    field[(player.x, player.y)].player = True
    print(f"Moved to {(player.x, player.y)}")
    if field[(player.x, player.y)].monster is not None:
        encounter(player.x, player.y)
    return

def down_func(args):
    if len(shlex.split(args)) > 0:
        print("Invalid arguments")
        return
    field[(player.x, player.y)].player = False
    player.y = (player.y + 1) % 10
    field[(player.x, player.y)].player = True
    print(f"Moved to {(player.x, player.y)}")
    if field[(player.x, player.y)].monster is not None:
        encounter(player.x, player.y)
    return

def left_func(args):
    if len(shlex.split(args)) > 0:
        print("Invalid arguments")
        return
    field[(player.x, player.y)].player = False
    player.x = (player.x - 1) % 10
    field[(player.x, player.y)].player = True
    print(f"Moved to {(player.x, player.y)}")
    if field[(player.x, player.y)].monster is not None:
        encounter(player.x, player.y)
    return

def right_func(args):
    if len(shlex.split(args)) > 0:
        print("Invalid arguments")
        return
    field[(player.x, player.y)].player = False
    player.x = (player.x + 1) % 10
    field[(player.x, player.y)].player = True
    print(f"Moved to {(player.x, player.y)}")
    if field[(player.x, player.y)].monster is not None:
        encounter(player.x, player.y)
    return

def addmon_func(args):
    commands = shlex.split(args)
    length_commands = len(commands)
    if length_commands != 8:
        print("Invalid arguments")
        return
    name, phrase = commands[0], ""
    x, y, hp = 0, 0, 0
    try:
        i = 1
        while i < 8:
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
        return
    if name not in list_cows() and name != "jgsbat":
        print("Cannot add unknown monster")
        return
    monster = Monster(name, x, y, phrase, hp)
    replaced_monster_flag = True if field[(x, y)].monster is not None else False
    field[(x, y)].monster = monster
    print(f"Added monster {name} to {(x, y)} saying {phrase}")
    if replaced_monster_flag:
        print("Replaced the old monster")
    return

def attack_func(args):
    commands = shlex.split(args)
    commands_length = len(commands)
    if commands_length != 3 and commands_length != 1:
        print("Invalid arguments")
        return
    weapon = "sword"
    monster_name = commands[0]
    if commands_length > 1:
        match commands[1]:
            case "with":
                weapon = commands[2]
            case _:
                print("Invalid arguments")
                return
    if field[(player.x, player.y)].monster is None:
        print("No monster here")
        return
    if field[(player.x, player.y)].monster.name != monster_name:
        print(f"No {monster_name} here")
        return
    if weapon not in weapons:
        print("Unknown weapon")
        return
    damage = weapons[weapon]
    if field[(player.x, player.y)].monster.hp > damage:
        print(f"Attacked {field[(player.x, player.y)].monster.name}, damage {damage} hp")
        field[(player.x, player.y)].monster.hp -= damage
        print(f"{field[(player.x, player.y)].monster.name} now has {field[(player.x, player.y)].monster.hp}")
    else:
        print(f"Attacked {field[(player.x, player.y)].monster.name}, damage {field[(player.x, player.y)].monster.hp} hp")
        print(f"{field[(player.x, player.y)].monster.name} died")
        field[(player.x, player.y)].monster = None
    return

#Game main class.

class Mud(cmd.Cmd):
    """
    Multi-user dungeon game!
    """
    prompt = "o-(====> "

    def do_up(self, args):
        """
        Go up on the board.
        Usage: up
        """
        up_func(args)
        pass
    
    def do_down(self, args):
        """
        Go down on the board.
        Usage: down
        """
        down_func(args)
        pass

    def do_left(self, args):
        """
        Go left on the board.
        Usage: left
        """
        left_func(args)
        pass
    
    def do_right(self, args):
        """
        Go right on the board.
        Usage: right
        """
        right_func(args)
        pass

    def do_addmon(self, args):
        """
        Add monster to the board.
        Usage: addmon NAME coords X Y hp HP hello HELLO
        """
        addmon_func(args)
        pass

    def do_attack(self, args):
        """
        Attack the monster in the current cell.
        Usage: attack MONSTER_NAME [with WEAPON]
        """
        attack_func(args)
        pass

    def complete_attack(self, text, line, begidx, endidx):
        tmp = shlex.split(line)
        if len(tmp) == 2:
            return [m for m in list_cows() if m.startswith(text)]
        elif len(tmp) == 4:
            return [w for w in weapons if w.startswith(text)]
        elif "with".startswith(text):
            return ["with"]

    def do_EOF(self, args):
        print("\n<<< Thank you for playing! >>>")
        return True

if __name__ == "__main__":
    print("<<< Welcome to Python-MUD 0.1 >>>")
    Mud().cmdloop()

