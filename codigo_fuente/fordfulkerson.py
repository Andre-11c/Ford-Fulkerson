import numpy as np
import math

with open('Dataset.json') as file:
    G = []
    for line in file:
        if line.startswith('-'):
            G.append([])
            continue
        nums = list(map(int, line.split()))
        G.append([(nums[i], nums[i+1]) for i in range(0, len(nums), 2)])

n = len(G)
G1 = np.full((n, n), np.nan)

for u in range(n):
    for v, w in G[u]:
        G1[u, v] = w

def findAugmentingPath(G, s, t):
    n = len(G)
    visited = [False]*n
    augPath = []

    def dfs(u, bottleNeck):
        visited[u] = True
        augPath.append(u)
        if u == t:
            return bottleNeck
        for v in range(n):
            if G[u, v] > 0 and not visited[v]:
                bn2 = dfs(v, bottleNeck if bottleNeck <= G[u, v] else G[u, v])
                if visited[t]:
                    return bn2
        augPath.pop()

    bottleNeck = dfs(s, math.inf)

    return augPath, bottleNeck

findAugmentingPath(G1, 0, 5)

def fordFulkerson(G, s, t):
    n = len(G)
    Gres = G.copy()
    for i in range(n):
        for j in range(n):
            if not np.isnan(Gres[i, j]) and np.isnan(Gres[j, i]):
                Gres[j, i] = 0
    Gflow = np.zeros((n, n))

    maxFlow = 0
    augmentingPath, bottleNeck = findAugmentingPath(Gres, s, t)
    while augmentingPath:
        for i in range(len(augmentingPath) - 1):
            u = augmentingPath[i]
            v = augmentingPath[i+1]
            Gres[u, v] -= bottleNeck
            Gres[v, u] += bottleNeck
            Gflow[u, v] += bottleNeck
        maxFlow += bottleNeck
        augmentingPath, bottleNeck = findAugmentingPath(Gres, s, t)

    return maxFlow, Gflow

maxFlow, G2 = fordFulkerson(G1, 0, 5)
print(maxFlow)
n = len(G2)
G3 = [[] for _ in range(n)]
for i in range(n):
    for j in range(n):
        if G2[i, j] > 0 and G2[i, j] != G2[j, i]:
            G3[i].append((j, G2[i, j]))

print(G3)


with open('FinalGraph.txt', 'w') as file:
    for row in G3:
        file.write(str(row) + '\n')

with open('FinalGraph.txt', 'r') as file:
    print(file.read())