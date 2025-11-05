from graph import Graph
import random


def sync_consensus(graph: Graph, eps=0.1, max_iters=200, tol=0.0001):
    values = [n.val for n in graph.nodes]
    history = [values.copy()]

    for _ in range(max_iters):
        for node in graph.nodes:
            new_values = []
            for node in graph.nodes:
                delta = sum(neighbor.val - node.val for neighbor in node.neighbors)
                new_values.append(node.val + eps * delta)

            for i, node in enumerate(graph.nodes):
                node.val = new_values[i]

            values = [n.val for n in graph.nodes]
            history.append(values.copy())

            if max(values) - min(values) < tol:
                break

        return history


def async_consensus(graph: Graph, max_iters=1000, tol=0.0001):
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
