import numpy as np
from src.graph import Graph


def additive_secret_share_matrix(graph: Graph):
    n = len(graph.nodes)

    # adjencency matrix
    A = np.zeros((n, n))
    for node in graph.nodes:
        for neighbor in node.neighbors:
            A[node.id, neighbor.id] = 1

    R = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if A[i, j] == 1:
                R[i, j] = np.random.uniform(-1, 1)

    s = np.array([node.val for node in graph.nodes])

    ones = np.ones(n)
    # s' = s - R·1 + Rᵀ·1 using np.dot() for matrix multiplication
    s_shared = s - np.dot(R, ones) + np.dot(R.T, ones)

    for i, node in enumerate(graph.nodes):
        node.val = s_shared[i]
