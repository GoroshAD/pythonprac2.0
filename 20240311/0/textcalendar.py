import cmd, calendar

class Calen(cmd.Cmd):
    """
    Calendar.
    """
    prompt = "=)"
    months = {m.name: m.value for m in calendar.Month}
    def do_prmonth(self, args):
        calendar.TextCalendar().prmonth(*map(int, args.split()))

    def do_pryear(self, args):
        calendar.TextCalendar().pryear(*map(int, args.split()))

    def do_EOF(self, args):
        return True
    
    def complete_prmonth(self, text, line, begidx, endidx):
        if len(line.split()) >= 2:
            return [c for c in month if c.startswith(text)]

    def emptyline(self):
        pass

if __name__ == "__main__":
    Calen().cmdloop()
