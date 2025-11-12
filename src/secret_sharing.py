import numpy as np
from src.graph import Graph

# Just a super large prime
P = 2**31 - 1


def additive_secret_share_matrix(graph: Graph):
    n = len(graph.nodes)

    # get initial secrets s_i as integers
    s = np.array([int(node.initial_val) for node in graph.nodes])

    # will store random values shared from i to j
    R_shares = np.zeros((n, n), dtype=np.int64)

    # using a super long range generate random shares r_i^j for all directed edges (i,j)
    # random shares must be between [0, P-1]
    r_range = 1_000_000

    for i in range(n):
        for neighbor in graph.nodes[i].neighbors:
            j = neighbor.id
            # ensure r_i^j is only generated once per directed edge
            if R_shares[i, j] == 0:
                r_ij = np.random.randint(0, r_range)
                R_shares[i, j] = r_ij

    r = np.zeros(n, dtype=np.int64)
    for i in range(n):
        r_i_sum = 0

        # iterate over neighbors N_i
        for neighbor in graph.nodes[i].neighbors:
            j = neighbor.id

            # r_i^j and r_j^i (sent to i from j)
            r_ij = R_shares[i, j]
            r_ji = R_shares[j, i]

            # r_i = sum (r_i^j - r_j^i) mod P
            difference_mod_p = np.mod(r_ij - r_ji, P)
            r_i_sum = np.mod(r_i_sum + difference_mod_p, P)

        r[i] = r_i_sum

    # calculate the shared secret s_i^r = (s_i + r_i) mod p
    s_shared = np.mod(s + r, P)

    # update node vals for next step
    for i, node in enumerate(graph.nodes):
        node.initial_s = s[i]
        node.r_mask = r[i]
        node.s_shared = s_shared[i]

        node.val = float(s_shared[i])
