import requests
import sys
import re
import pprint
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import time
from fast_sugiyama import from_edges

matplotlib.use("MacOSX")



fig, ax = plt.subplots(figsize=(16, 10))

fig.patch.set_facecolor("#0b1120")
ax.set_facecolor("#0b1120")


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

scores = {}

def get_risk_score(node):

    impact = G.in_degree(node)
    complexity = G.out_degree(node)
    transitive = len(nx.descendants(G, node))

    return (
        0.5 * impact +
        0.2 * complexity +
        0.3 * transitive
    )

for node in G.nodes():
    scores[node] = get_risk_score(node)

max_score = max(scores.values(), default=1)

for node in scores:
    scores[node] = scores[node] / max_score * 100

# Draw the graph
pos = from_edges(G.edges()).to_dict()

nx.draw_networkx_edges(
    G,
    pos,
    edge_color="#64748b",
    width=1.8,
    alpha=0.55,
    arrows=True,
    arrowsize=18,
    arrowstyle="-|>",
    node_shape="s"
)

nx.draw_networkx_nodes(
    G,
    pos,
    ax=ax,
    node_color="#6366f1",
    node_size=2500,
    edgecolors="#a5b4fc",
    linewidths=2.5,
    alpha=0.95,
    node_shape="s"
)

nx.draw_networkx_labels(
    G,
    pos,
    ax=ax,
    labels={node: f"{node}\n{round(scores[node], 2)}" for node in scores},
    font_size=8,
    font_weight="bold",
    font_color="white"
)


ax.set_title(
    f"Dependency Graph",
    fontsize=20,
    fontweight="bold",
    color="white",
    pad=25
)

stats = (
    f"Packages: {G.number_of_nodes()}    "
    f"Dependencies: {G.number_of_edges()}"
)

fig.text(
    0.5,
    0.03,
    stats,
    ha="center",
    fontsize=12,
    color="#94a3b8"
)


plt.tight_layout()
plt.show()

time.sleep(5)

exit()
