import matplotlib.pyplot as plt
import math
import networkx as nx
from scipy.spatial.distance import *
from util import generateGraph, pathDistance

def BruteForce1(g, R, S):
    if(len(S) == 0):
        minCost = pathDistance(g, R)
    else:
        minCost = float("inf")
        for i in range(0, len(S)):
            tmp = S[i]
            R.append(S[i])
            del S[i]
            minCost = min(minCost, BruteForce1(g, R,S))
            S.append(tmp)
            del R[-1]
    return minCost

def BruteForce2(g, A, l, lengthSoFar):
    n = len(A)
    if(l == n-1):
        minCost = lengthSoFar + g[A[-1]][A[0]]['weight']
    else:
        minCost = float("inf")
        for i in range(l+1, n):
            tmp = A[l+1]
            A[l+1] = A[i]
            A[i] = tmp
            newLength = lengthSoFar + g[A[l]][A[l+1]]['weight']
            minCost = min(minCost, BruteForce2(g, A, l+1, newLength))
            A[i] = A[l+1]
            A[l+1] = tmp
    return minCost

def main() :
    maxNode = 10
    g = generateGraph('./instances/bayg29.tsp', maxNode)
    R = [1]
    S = range(2,maxNode+1)
    print(BruteForce1(g, R,S))
    A = range(1,maxNode+1)
    print(BruteForce2(g, A, 0, 0))
    nx.draw(g, with_labels=True, font_weight='bold')
    plt.show()

if __name__ == "__main__":
    main()
