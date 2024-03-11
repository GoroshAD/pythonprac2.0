import cmd

class Echoer(cmd.Cmd):
    """
    HI HI HI HA
    """
    prompt = ":->"
    words = "one", "two", "three", "four", "five"

    def do_echo(self, args):
        print(args)

    def complete_echo(self, text, line, begidx, endidx):
        return [c for c in self.words if c.startswith(text)]

    def do_EOF(self, args):
        return True

    def emptyline(self):
        pass
if __name__ == "__main__":
    Echoer().cmdloop()

