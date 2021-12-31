from django.shortcuts import render
from utils import restful
import networkx as nx
from networkx.utils import py_random_state
import networkx as nx
import numpy as np
from random import random

def scaleFreeNetworks(request):
    n = int(request.GET.get("n"))
    m = int(request.GET.get("m"))
    g = nx.barabasi_albert_graph(n, m)
    g_objects = {"nodes": [], "links": []}
    deg = get_degree(g)
    for i in g.nodes:
        g_objects["nodes"].append({"id": i, "deg": deg[i]})

    for i in g.edges:
        g_objects["links"].append({"source": i[0], "target": i[1]})
    return restful.result(data=g_objects)


def smallWorldNetworks(request):
    n = int(request.GET.get("n"))
    k = int(request.GET.get("k"))
    p = float(request.GET.get("p"))
    g = nx.newman_watts_strogatz_graph(n, k, p)
    g_objects = {"nodes": [], "links": []}
    deg = get_degree(g)
    for i in g.nodes:
        g_objects["nodes"].append({"id": i, "deg": deg[i]})

    for i in g.edges:
        g_objects["links"].append({"source": i[0], "target": i[1]})
    return restful.result(data=g_objects)


def randomNetworks(request):
    n = int(request.GET.get("n"))
    p = float(request.GET.get("p"))
    g = nx.erdos_renyi_graph(n, p)
    g_objects = {"nodes": [], "links": []}
    deg = get_degree(g)
    for i in g.nodes:
        g_objects["nodes"].append({"id": i, "deg": deg[i]})

    for i in g.edges:
        g_objects["links"].append({"source": i[0], "target": i[1]})
    return restful.result(data=g_objects)


def get_degree(g):
    deg = nx.degree(g)
    v = {}
    for i in deg:
        v[i[0]] = i[1]
    return v


def _random_subset(seq, m, rng):
    targets = set()
    while len(targets) < m:
        x = rng.choice(seq)
        targets.add(x)
    return targets


def evolution_networks(request):
    n = int(request.GET.get("n"))
    m = int(request.GET.get("m"))
    v = []
    for i in random_graph(n, m):
        v.append(get_graph_tuple(i))
    return restful.result(message= {"length": len(v)},data=v)

def get_graph_tuple(g):
    g_objects = {"nodes": [], "links": []}
    deg = get_degree(g)
    for i in g.nodes:
        g_objects["nodes"].append({"id": i, "deg": deg[i]})

    for i in g.edges:
        g_objects["links"].append({"source": i[0], "target": i[1]})
    return g_objects


@py_random_state(2)
def random_graph(n,m, seed=None):
    if m < 1 or m >= n:
        raise nx.NetworkXError(
            f"Barabási–Albert network must have m >= 1 and m < n, m = {m}, n = {n}"
        )

    # Add m initial nodes (m0 in barabasi-speak)
    G = nx.empty_graph(m)
    # Target nodes for new edges
    targets = list(range(m))
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes = []
    # Start adding the other n-m nodes. The first node is m.
    source = m
    while source < n:
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source] * m, targets))
        yield G
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source] * m)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachment)
        targets = _random_subset(repeated_nodes, m, seed)
        source += 1


def osmnx_map(request):
    g = nx.read_gml("./networks/vvv_drive.gml", label="id")
    # g_objects = {"nodes": [{"id":0},{"id":1}], "links": [{"source":0, "target":1}]}
    g_objects = {"nodes": [], "links": []}
    xx = []
    yy = []
    for i in g.nodes:
        v = g.nodes[i]
        xx.append(-float(v["x"]))
        yy.append(float(v["y"]))
    xx = np.array(xx)
    yy = np.array(yy)

    xx = (xx - np.min(xx)) / (np.max(xx) - np.min(xx))
    yy = (yy - np.min(yy)) / (np.max(yy) - np.min(yy))


    for i in g.nodes:

        # g_objects["nodes"].append({"id": i, "x": -float(v["x"]), "y": float(v["y"])})
        # g_objects["nodes"].append({"id": i, "x": random(), "y": random()})
        g_objects["nodes"].append({"id": i, "x": 500 * xx[i], "y": 500 * yy[i]})





    for i in g.edges:
        g_objects["links"].append({"source": i[0], "target": i[1]})
    return restful.result(data=g_objects)
