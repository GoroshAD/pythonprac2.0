import cmd, sys, socket, shlex
from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO

#Constants and dictionaries

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

weapons ={"sword": 10, "spear": 15, "axe": 20}

#Game client's functions.

def move_func(args, dest, socket):
    if len(shlex.split(args)) > 0:
        print("Invalid arguments")
        return
    match dest:
        case "up":
            socket.sendall((f"move {0} {-1}").encode())
        case "down":
            socket.sendall((f"move {0} {1}").encode())
        case "left":
            socket.sendall((f"move {-1} {0}").encode())
        case "right":
            socket.sendall((f"move {1} {0}").encode())
        case _:
            print("Invalid arguments")
            return
    answer = shlex.split(socket.recv(1024).rstrip().decode())
    print(f"Moved to {(int(answer[0]), int(answer[1]))}")
    if answer[2] != "None": #encounter
        if answer[2] == "jgsbat":
            print(cowsay(answer[3], cowfile=read_dot_cow(JGSBAT)))
        else:
            print(cowsay(answer[3], cow=answer[2]))
    return

def addmon_func(args, socket):
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
    socket.sendall((f"addmon {name} {x} {y} {phrase} {hp}").encode())
    answer = shlex.split(socket.recv(1024).rstrip().decode())
    print(f"Added monster {name} to {(x, y)} saying {phrase}")
    if eval(answer[0]):
        print("Replaced the old monster")
    return

def attack_func(args, socket):
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
    if weapon not in weapons:
        print("Unknown weapon")
        return
    damage = weapons[weapon]
    socket.sendall((f"attack {monster_name} {damage}").encode())
    answer = shlex.split(socket.recv(1024).rstrip().decode())
    if not eval(answer[0]):
        print(f"No {monster_name} here")
        return
    print(f"Attacked {monster_name}, damage {int(answer[1])} hp")
    if int(answer[2]) == 0:
        print(f"{monster_name} died")
    else:
        print(f"{monster_name} now has {int(answer[2])}")
    return

#Game main class.

class Mud(cmd.Cmd):
    """
    Multi-user dungeon game!
    """
    prompt = "o-(====> "
    socket = None
    
    def __init__(self, socket):
        super().__init__()
        self.socket = socket

    def do_up(self, args):
        """
        Go up on the board.
        Usage: up
        """
        move_func(args, "up", self.socket)
        pass
    
    def do_down(self, args):
        """
        Go down on the board.
        Usage: down
        """
        move_func(args, "down", self.socket)
        pass

    def do_left(self, args):
        """
        Go left on the board.
        Usage: left
        """
        move_func(args, "left", self.socket)
        pass
    
    def do_right(self, args):
        """
        Go right on the board.
        Usage: right
        """
        move_func(args, "right", self.socket)
        pass

    def do_addmon(self, args):
        """
        Add monster to the board.
        Usage: addmon NAME coords X Y hp HP hello HELLO
        """
        addmon_func(args, self.socket)
        pass

    def do_attack(self, args):
        """
        Attack the monster in the current cell.
        Usage: attack MONSTER_NAME [with WEAPON]
        """
        attack_func(args, self.socket)
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
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1338 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        Mud(s).cmdloop()

