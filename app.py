import requests
import sys
import re
import pprint
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


names=set()
def parser():
    with open(sys.argv[1]) as file:
        content=file.read()
        data=re.findall("import\\s+(\\w+)|from\\s+(\\w+)",content)
        for lib in data:
            currname=lib[0]
            names.add(currname)
        return

parser()
# print(names)
pnamedeps=set()

global_edgelist=set()

def populate_depslist(pkgname):
    response = requests.get(f"https://pypistats.com/api/dependencies?package={pkgname}")
    # print (response.json())
    data = response.json()["depends_on"]
    # print(type(data))
    # print(data)
    for i in data:
        # print(i)
        edge=(pkgname,i["name"])
        global_edgelist.add(edge)
        populate_depslist(i["name"])
    return

for i in names:
    populate_depslist(i)
print(global_edgelist)

# Create a directed graph
G = nx.DiGraph()

# Add dependency relationships
G.add_edges_from(global_edgelist)

deps = []
packages = set()
for (a,b) in global_edgelist:
    packages.add(a)
    packages.add(b)

package = 'jupyter-client' # Insert actual package name here

for a,b in global_edgelist:
    if a == package and b not in deps:
        deps.append(a)
    if b == package and a not in deps:
        deps.append(b)

print(f"Dependency risk: {len(deps)/len(packages)}")
# Draw the graph
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=2000,
    node_color="lightblue",
    arrows=True,
    font_size=12
)

plt.show()
