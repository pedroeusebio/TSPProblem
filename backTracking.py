import matplotlib.pyplot as plt
import math
import networkx as nx
from scipy.spatial.distance import *
from util import generateGraph, generateGraph2, pathDistance


def BackTracking(g, A, l, lengthSoFar, minCost, bestSol):
    n = len(A)
    if(l == n-1):
        if(minCost > lengthSoFar + g[A[-1]][A[0]]['weight']):
            bestSol = A
        minCost = min(minCost, lengthSoFar + g[A[-1]][A[0]]['weight'])
    else:
        for i in range(l+1, n):
            tmp = A[l+1]
            A[l+1] = A[i]
            A[i] = tmp
            newLength = lengthSoFar + g[A[l]][A[l+1]]['weight']
            if (newLength >= minCost) :
                A[i] = A[l+1]
                A[l+1] = tmp
                continue
            else:
                newSol = BackTracking(g, A, l+1, newLength, minCost, bestSol)
                if(newSol[0] < minCost):
                    print(newSol[1])
                    bestSol = newSol[1]
                minCost = min(minCost, newSol[0])
                A[i] = A[l+1]
                A[l+1] = tmp
    return minCost, bestSol


def main() :
    maxNode = 5
    g = generateGraph2('./instances/test.tsp', 5, maxNode)
    A = range(1, maxNode+1)
    sol = BackTracking(g, A, 0, 0, float("inf"), [])
    print(sol[0])
    print(sol[1])
    print(pathDistance(g,sol[1]))
    print(pathDistance(g, [1, 3, 2, 4, 5]))
    nx.draw(g, with_labels=True, font_weight='bold')
    plt.show()

if __name__ == "__main__":
    main()
