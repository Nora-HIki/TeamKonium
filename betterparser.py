import re

<<<<<<< HEAD
with open("./input.txt") as file:
    content=file.read()
    data=re.findall("^import\s(\S+)|from\s(\S+)",content)

print(data)
=======
with open("./test.txt", "r") as file:
    content = file.read()
    patterns = re.findall(r'^import\s(\S+)|from\s(\S+)', content)
    print(patterns)
>>>>>>> refs/remotes/origin/main
