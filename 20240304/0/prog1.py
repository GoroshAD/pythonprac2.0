import shlex

name = shlex.split(input("ФИО: "))
place = shlex.split(input("место: "))
print("register ",shlex.join(name + place))
