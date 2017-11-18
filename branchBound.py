import matplotlib.pyplot as plt
import math
import networkx as nx
import heapq
import copy
from scipy.spatial.distance import *
from util import generateGraph, generateGraph2, pathDistance

class Node:
    pass
    def __init__(self, parentMatrix, path, level, i, j, N):
        self.path = copy.deepcopy(path)
        self.reducedMatrix = copy.deepcopy(parentMatrix)
        if(level != 0):
            self.path.append((i,j))
        k = 0
        while(level != 0 and k < N):
            self.reducedMatrix[i][k] = float("inf")
            self.reducedMatrix[k][j] = float("inf")
            k+=1
        self.reducedMatrix[j][0] = float("inf")
        self.level = level
        self.vertex = j


def rowReduction(reducedMatrix, N):
    row = [float("inf")] * N

    for i in range(0,N):
        for j in range(0,N):
            if(reducedMatrix[i][j] < row[i]):
                row[i] = reducedMatrix[i][j]

    for i in range(0,N):
        for j in range(0,N):
            if(reducedMatrix[i][j] != float("inf") and row[i] != float("inf")):
                reducedMatrix[i][j] -= row[i]
    return row

def columnReduction(reducedMatrix, N):
    col = [float("inf")] * N
    for i in range(0,N):
        for j in range(0,N):
            if(reducedMatrix[i][j] < col[j]):
                col[j] = reducedMatrix[i][j]

    for i in range(0,N):
        for j in range(0,N):
            if(reducedMatrix[i][j] != float("inf") and col[j] != float("inf")):
                reducedMatrix[i][j] -= col[j]

    return col

def calculateCost(reducedMatrix, N):
    cost = 0
    row = rowReduction(reducedMatrix, N)
    col = columnReduction(reducedMatrix, N)
    for i in range(0, N):
        if(row[i] != float("inf")):
            cost += row[i]
        if(col[i] != float("inf")):
            cost += col[i]
    return cost

def printPath(path):
    for i in range(len(path)):
        print(path[i][0] + 1 , " -> ", path[i][1] +1 )


def BranchBound(G, N):
    # N  = G.number_of_nodes()
    pq = []

    path = []
    root = Node(G, path, 0, -1, 0, N)
    root.cost = calculateCost(root.reducedMatrix, N)
    heapq.heappush(pq, (root.cost, root))

    while(len(pq) > 0):
        min = heapq.heappop(pq)
        i = min[1].vertex
        if(min[1].level == N - 1 ):
            min[1].path.append((i, 0))
            printPath(min[1].path)
            return min[1].cost
        for j in range(0, N):
            child = Node(min[1].reducedMatrix, min[1].path, min[1].level + 1 , i, j, N)
            child.cost = min[1].cost + min[1].reducedMatrix[i][j] + calculateCost(child.reducedMatrix, N)
            heapq.heappush(pq, (child.cost, child))

def main() :
    maxNode = 5
    # costMatrix = [
    #     [float("inf"), 10 ,8 ,9 ,7],
    #     [10, float("inf"), 10, 5, 6],
    #     [8, 10, float("inf"), 8, 9],
    #     [9, 5, 8, float("inf"), 6],
    #     [7, 6, 9, 6, float("inf")]
    # ]
    costMatrix = [
        [ float("inf") ,29 ,82 ,46 ,68 ,52 ,72 ,42 ,51 ,55 ,29 ,74 ,23 ,72 ,46 ],
        [ 29 ,float("inf") ,55 ,46 ,42 ,43 ,43 ,23 ,23 ,31 ,41 ,51 ,11 ,52 ,21 ],
        [ 82 ,55 ,float("inf") ,68 ,46 ,55 ,23 ,43 ,41 ,29 ,79 ,21 ,64 ,31 ,51 ],
        [ 46 ,46 ,68 ,float("inf") ,82 ,15 ,72 ,31 ,62 ,42 ,21 ,51 ,51 ,43 ,64 ],
        [ 68 ,42 ,46 ,82 ,float("inf") ,74 ,23 ,52 ,21 ,46 ,82 ,58 ,46 ,65 ,23 ],
        [ 52 ,43 ,55 ,15 ,74 ,float("inf") ,61 ,23 ,55 ,31 ,33 ,37 ,51 ,29 ,59 ],
        [ 72 ,43 ,23 ,72 ,23 ,61 ,float("inf") ,42 ,23 ,31 ,77 ,37 ,51 ,46 ,33 ],
        [ 42 ,23 ,43 ,31 ,52 ,23 ,42 ,float("inf") ,33 ,15 ,37 ,33 ,33 ,31 ,37 ],
        [ 51 ,23 ,41 ,62 ,21 ,55 ,23 ,33 ,float("inf") ,29 ,62 ,46 ,29 ,51 ,11 ],
        [ 55 ,31 ,29 ,42 ,46 ,31 ,31 ,15 ,29 ,float("inf") ,51 ,21 ,41 ,23 ,37 ],
        [ 29 ,41 ,79 ,21 ,82 ,33 ,77 ,37 ,62 ,51 ,float("inf") ,65 ,42 ,59 ,61 ],
        [ 74 ,51 ,21 ,51 ,58 ,37 ,37 ,33 ,46 ,21 ,65 ,float("inf") ,61 ,11 ,55 ],
        [ 3 ,11 ,64 ,51 ,46 ,51 ,51 ,33 ,29 ,41 ,42 ,61 ,float("inf") ,62 ,23 ],
        [ 72 ,52 ,31 ,43 ,65 ,29 ,46 ,31 ,51 ,23 ,59 ,11 ,62 ,float("inf") ,59 ],
        [ 46 ,21 ,51 ,64 ,23 ,59 ,33 ,37 ,11 ,37 ,61 ,55 ,23 ,59 ,float("inf") ],
    ]

    print(BranchBound(costMatrix, 15))

if __name__ == "__main__":
    main()
