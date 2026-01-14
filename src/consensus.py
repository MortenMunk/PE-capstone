from src.graph import Graph
import random
import numpy as np

tol = 0.000001


def sync_consensus(graph: Graph, max_iters=2000, tol=tol):
    W = weight_matrix(graph)

    x = np.array([n.val for n in graph.nodes])
    history = [x.copy()]

    for _ in range(max_iters):
        x_next = np.dot(W, x)
        history.append(x_next.copy())

        if has_converged(x_next, tol):
            break
        x = x_next

    for i, node in enumerate(graph.nodes):
        node.val = x[i]

    return history


def weight_matrix(graph):
    n = len(graph.nodes)
    max_degree = max(len(node.neighbors) for node in graph.nodes)
    alpha = 1.0 / (max_degree + 1)

    W = np.zeros((n, n))
    for node in graph.nodes:
        i = node.id
        degree = len(node.neighbors)
        W[i, i] = 1.0 - (degree * alpha)
        for neighbor in node.neighbors:
            W[i, neighbor.id] = alpha
    return W


def async_consensus(graph: Graph, max_iters=20000, tol=tol):
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

        if has_converged(values, tol):
            break

    return history


def has_converged(values, tol):
    return (np.max(values) - np.min(values)) < tol
