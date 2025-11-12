from src.graph import Graph
import random
import numpy as np

tol = 0.00001


def sync_consensus(graph: Graph, eps=0.1, max_iters=2000, tol=tol):
    W = weight_matrix(graph, eps)

    x = np.array([n.val for n in graph.nodes])
    history = [x.copy()]

    for _ in range(max_iters):
        x_next = np.dot(W, x)
        history.append(x_next.copy())

        if np.max(np.abs(x_next - x)) < tol:
            break
        x = x_next

    for i, node in enumerate(graph.nodes):
        node.val = x[i]

    return history


def weight_matrix(graph, eps=0.1):
    n = len(graph.nodes)
    A = np.zeros((n, n))
    for node in graph.nodes:
        for neighbor in node.neighbors:
            A[node.id, neighbor.id] = 1

    # Degree matrix
    D = np.diag(np.sum(A, axis=1))
    # Laplacian graph
    L = D - A
    # Static weight matrix
    W = np.eye(n) - eps * L
    return W


def async_consensus(graph: Graph, max_iters=1000, tol=tol):
    values = [n.val for n in graph.nodes]
    history = [values.copy()]

    for _ in range(max_iters):
        i = random.choice(graph.nodes)
        j = random.choice(list(i.neighbors))
        avg = (i.val + j.val) / 2
        i.val = avg
        j.val = avg

        values = [n.val for n in graph.nodes]
        history.append(values.copy())

        if max(values) - min(values) < tol:
            break

    return history
