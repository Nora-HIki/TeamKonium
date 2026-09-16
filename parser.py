import re

with open("./input.txt") as file:
    content=file.read()
    data=re.findall("^import\s(\S+)|from\s(\S+)",content)

print(data)
