import random
import copy
import math
import operator

def cost(costMatrix, path):
    distance = 0
    if len(path) > 0 :
        for i in range(0, len(path)-1):
            distance += costMatrix[path[i]][path[i+1]]
        distance += costMatrix[path[-1]][path[0]]
        return distance
    else:
        return float("inf")

def stochasticTwoOpt(permutation):
    perm = copy.deepcopy(permutation)
    c1, c2 = random.sample(range(len(perm)), 2)
    ex = [c1]
    if(c1 == 0):
        ex.append(len(perm)-1)
    else:
        ex.append(c1-1)
    if(c1 == len(perm)-1):
        ex.append(0)
    else:
        ex.append(c1+1)
    while c2 in ex:
        c2 = random.choice(range(len(perm)))
    if c2 < c1:
        tmp = c2
        c2 = c1
        c1 = tmp
    newOrder = perm[:c1]
    newOrder+= perm[c1:c2+1][::-1]
    newOrder+= perm[c2+1:]
    return newOrder


def localSearch(costMatrix, best, maxImprov, maxIter):
    newBest = copy.deepcopy(best)
    improv = 0
    it = 0
    while improv <= maxImprov and it <= maxIter:
        candidate = {}
        candidate["vector"] = stochasticTwoOpt(newBest["vector"])
        candidate["cost"] = cost(costMatrix, candidate["vector"])
        if(candidate["cost"] < newBest["cost"]):
            improv += 1
            newBest = candidate
        it += 1
    return newBest

def greedyRandomizedConstruction(costMatrix, alpha):
    candidate = {};
    allpoints = range(0,len(costMatrix))
    candidate["vector"] = [random.choice(allpoints)]
    while len(candidate["vector"]) < len(allpoints):
        candidates = copy.deepcopy(allpoints)
        for i in range(len(candidate["vector"])):
            try:
                candidates.remove(candidate["vector"][i])
            except ValueError:
                continue
        costs = []
        for i in candidates:
            costs.append((i, costMatrix[candidate["vector"][-1]][i]))
        rcl = []
        maxC = max(costs, key=operator.itemgetter(1))
        minC = min(costs, key=operator.itemgetter(1))
        for i in range(len(costs)):
            if(costs[i][1] <= minC[1] + alpha*(maxC[1]-minC[1])):
                rcl.append(costs[i][0])
        candidate["vector"].append(random.choice(rcl))
    candidate["cost"] = cost(costMatrix, candidate["vector"])
    return candidate

def GRASP(costMatrix, maxIter, alpha, maxImprov):
    sBest = None
    for i in range(maxIter):
        sCandidate = greedyRandomizedConstruction(costMatrix, alpha)
        newCandidate = localSearch(costMatrix, sCandidate, maxImprov, maxIter)
        if( sBest == None or sCandidate["cost"] < sBest["cost"]):
            sBest = sCandidate
    return sBest

def main():
    costMatrix = [
        [float("inf"), 10 ,8 ,9 ,7],
        [10, float("inf"), 10, 5, 6],
        [8, 10, float("inf"), 8, 9],
        [9, 5, 8, float("inf"), 6],
        [7, 6, 9, 6, float("inf")]
    ]
    # costMatrix = [
    #     [ float("inf") ,29 ,82 ,46 ,68 ,52 ,72 ,42 ,51 ,55 ,29 ,74 ,23 ,72 ,46 ],
    #     [ 29 ,float("inf") ,55 ,46 ,42 ,43 ,43 ,23 ,23 ,31 ,41 ,51 ,11 ,52 ,21 ],
    #     [ 82 ,55 ,float("inf") ,68 ,46 ,55 ,23 ,43 ,41 ,29 ,79 ,21 ,64 ,31 ,51 ],
    #     [ 46 ,46 ,68 ,float("inf") ,82 ,15 ,72 ,31 ,62 ,42 ,21 ,51 ,51 ,43 ,64 ],
    #     [ 68 ,42 ,46 ,82 ,float("inf") ,74 ,23 ,52 ,21 ,46 ,82 ,58 ,46 ,65 ,23 ],
    #     [ 52 ,43 ,55 ,15 ,74 ,float("inf") ,61 ,23 ,55 ,31 ,33 ,37 ,51 ,29 ,59 ],
    #     [ 72 ,43 ,23 ,72 ,23 ,61 ,float("inf") ,42 ,23 ,31 ,77 ,37 ,51 ,46 ,33 ],
    #     [ 42 ,23 ,43 ,31 ,52 ,23 ,42 ,float("inf") ,33 ,15 ,37 ,33 ,33 ,31 ,37 ],
    #     [ 51 ,23 ,41 ,62 ,21 ,55 ,23 ,33 ,float("inf") ,29 ,62 ,46 ,29 ,51 ,11 ],
    #     [ 55 ,31 ,29 ,42 ,46 ,31 ,31 ,15 ,29 ,float("inf") ,51 ,21 ,41 ,23 ,37 ],
    #     [ 29 ,41 ,79 ,21 ,82 ,33 ,77 ,37 ,62 ,51 ,float("inf") ,65 ,42 ,59 ,61 ],
    #     [ 74 ,51 ,21 ,51 ,58 ,37 ,37 ,33 ,46 ,21 ,65 ,float("inf") ,61 ,11 ,55 ],
    #     [ 3 ,11 ,64 ,51 ,46 ,51 ,51 ,33 ,29 ,41 ,42 ,61 ,float("inf") ,62 ,23 ],
    #     [ 72 ,52 ,31 ,43 ,65 ,29 ,46 ,31 ,51 ,23 ,59 ,11 ,62 ,float("inf") ,59 ],
    #     [ 46 ,21 ,51 ,64 ,23 ,59 ,33 ,37 ,11 ,37 ,61 ,55 ,23 ,59 ,float("inf") ],
    # ]
    maxIter = 500
    maxImprov = 50
    alpha = 0.3
    best = GRASP(costMatrix, maxIter, alpha, maxImprov)
    print(best)

if __name__ == "__main__":
    main()
