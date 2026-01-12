import numpy as np
from src.graph import Graph


def additive_secret_share_matrix(graph: Graph, r_range=1000):
    n = len(graph.nodes)
    # Track adjustments for each node
    adjustments = np.zeros(n)

    for i, node in enumerate(graph.nodes):
        # Requirement: Draw random numbers equal to number of neighbors
        for neighbor in node.neighbors:
            j = neighbor.id
            # To ensure consistency, we generate r_ij and subtract it from i, add to j
            if i < j:  # Process each edge only once to exchange the share
                r_ij = np.random.uniform(-r_range, r_range)
                adjustments[i] -= r_ij  # Subtracting sent number
                adjustments[j] += r_ij  # Adding received number

    for i, node in enumerate(graph.nodes):
        node.val = node.initial_val + adjustments[i]
