import networkx as nx
import math
from scipy.spatial.distance import *

def generateGraph(path, maxNode):
    g = nx.Graph()
    file = open (path, 'r')
    a = []
    # for i in range(0,7):
    #     file.readline()
    line = file.readline()
    distanceMatrix = []
    while line != "EOF":
        node = line.split(" ")
        a.append([float(node[1]), float(node[2])])
        g.add_node(int(node[0]))
        line = file.readline()
        if(int(node[0]) >= maxNode):
            break
    for i in range(0,min(len(a), maxNode)):
        distI = []
        for j in range(i, min(len(a), maxNode)):
            if(i != j) :
                distance = euclidean(a[i],[j])
                g.add_edge(i+1, j+1, weight=distance)
    file.close()
    return g

def pathDistance(g, path):
    distance = 0
    for i in range(0, len(path)-1):
        distance += g[path[i]][path[i+1]]['weight']
    distance +=g[path[-1]][path[0]]['weight']
    return distance
