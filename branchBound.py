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
    row = [None] * N
    for i in range(0,N):
        row[i] = float("inf")
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
    col = [None] * N
    for j in range(0,N):
        col[j] = float("inf")
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
        print(path[i][0], " -> ", path[i][1])


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
    costMatrix = [
        [float("inf"), 10 ,8 ,9 ,7],
        [10, float("inf"), 10, 5, 6],
        [8, 10, float("inf"), 8, 9],
        [9, 5, 8, float("inf"), 6],
        [7, 6, 9, 6, float("inf")]
    ]
    # costMatrix = [
    #     [float("inf"), 20 ,30 ,10 ,11],
    #     [15, float("inf"), 16, 4, 2],
    #     [3, 5, float("inf"), 2, 4],
    #     [19, 6, 15, float("inf"), 3],
    #     [16, 4, 7, 16, float("inf")]
    # ]
    # g = generateGraph2('./instances/test.tsp', 5, maxNode)
    print(BranchBound(costMatrix, maxNode))

if __name__ == "__main__":
    main()
