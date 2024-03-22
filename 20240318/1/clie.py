import cmd, sys, socket, shlex
import cowsay

#Constants

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

#Game client's functions.

def move_func(args, dest):
    if len(shlex.split(args)) > 0:
        print("Invalid arguments")
        return
    match dest:
        case "up":
            self.socket.sendall((" ".join(["move", "0", "-1"])).encode())
        case "down":
            self.socket.sendall((" ".join(["move", "0", "1"])).encode())
        case "left":
            self.socket.sendall((" ".join(["move", "-1", "0"])).encode())
        case "right":
            self.socket.sendall((" ".join(["move", "1", "0"])).encode())
        case _:
            print("Invalid arguments")
            return
    answer = shlex.split(self.s.recv(1024).rstrip().decode())
    print(f"Moved to {(answer[0], answer[1])}")
    if len(answer) == 4:
        if answer[2] == "jgsbat":
        print(cowsay(answer[3], cowfile=read_dot_cow(JGSBAT)))
    else:
        print(cowsay(answer[3], cow=answer[2]))
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
    self.socket.sendall((f"{name} {x} {y} {hello} {hp}")).encode())
    answer = shlex.split(self.s.recv(1024).rstrip().decode())
    print(f"Added monster {name} to {(x, y)} saying {phrase}")
    if answer[0]:
        print("Replaced the old monster")
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
        move_func(args, "up")
        pass
    
    def do_down(self, args):
        """
        Go down on the board.
        Usage: down
        """
        move_func(args, "down")
        pass

    def do_left(self, args):
        """
        Go left on the board.
        Usage: left
        """
        move_func(args, "left")
        pass
    
    def do_right(self, args):
        """
        Go right on the board.
        Usage: right
        """
        move_func(args, "right")
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
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        Mud(s).cmdloop()

