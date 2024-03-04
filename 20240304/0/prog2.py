import shlex

name = shlex.split(input("ФИО: "))
place = shlex.split(input("место: "))
res = shlex.join(["register"] + name + place)
print(shlex.quote(res))
