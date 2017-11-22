import networkx as nx
import matplotlib.pyplot as plt
import math
from scipy.spatial.distance import *

def generateGraph(path, maxNode):
    file = open (path, 'r')
    a = []
    line = file.readline()
    while line != "EOF":
        node = line.split(" ")
        a.append([float(node[1]), float(node[2])])
        line = file.readline()
        if(int(node[0]) >= maxNode):
            break
    g = []
    for i in range(min(len(a), maxNode)):
        field = []
        for j in range(min(len(a), maxNode)):
            field.append(float("inf"))
        g.append(field)
    for i in range(0,min(len(g), maxNode)):
        for j in range(i+1, min(len(g), maxNode)):
            distance = euclidean(a[i],a[j])
            g[i][j] = distance
            g[j][i] = distance
    file.close()
    return g

def generateGraph2(path, n, maxNode):
    g = nx.DiGraph()
    file = open (path, 'r')
    a = []
    for i in range(1, min(n+1, maxNode+1)):
        g.add_node(i)
    node = 1
    line = file.readline()
    while (line != "EOF\n" and node <= min(n, maxNode)):
        distances = line.split(" ")
        for i in range(min(len(distances), maxNode)):
            g.add_edge(node, i+1, weight=float(distances[i]))
        node += 1
        line = file.readline()

    print(g.number_of_nodes())
    print(g.number_of_edges())
    return g

def pathDistance(g, path):
    distance = 0
    for i in range(0, len(path)-1):
        distance += g[path[i]][path[i+1]]['weight']
    distance +=g[path[-1]][path[0]]['weight']
    return distance
