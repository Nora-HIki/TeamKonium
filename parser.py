import re

with open("./test.txt", "r") as file:
    content = file.read()
    patterns = re.findall(r'^import\s(\S+)|from\s(\S+)', content)
    print(patterns)
