import argparse
import numpy as np
import random

random.seed(42)
np.random.seed(42)

from src.consensus import async_consensus, sync_consensus
from src.graph import Graph
from src.secret_sharing import additive_secret_share_matrix
from src.utils import avg_error, plot_convergence, avg_error


def main():
    parser = argparse.ArgumentParser(description="Graph simulation")
    parser.add_argument(
        "--nodes", type=int, default=5, help="How many nodes in the graph?"
    )
    parser.add_argument(
        "--top",
        type=str,
        default="mesh",
        help="Which topology?",
        choices=["star", "mesh", "ring", "full"],
    )
    args = parser.parse_args()

    g = Graph(num_nodes=args.nodes, topology=args.top)
    g.assign_initial_values(20, 80)
    true_avg = np.mean([n.initial_val for n in g.nodes])
    additive_secret_share_matrix(g)

    print(
        f"Graph Topology: {args.top}, Nodes: {args.nodes}, True Average: {true_avg:.4f}"
    )

    # save history of initial vals
    initial_shared_vals = np.array([n.val for n in g.nodes])

    # synchronous
    print("Running synchornous...")
    for i, node in enumerate(g.nodes):
        # reset nodes to s_i^r
        node.val = initial_shared_vals[i]
    sync_history = sync_consensus(g)

    # asynchronous
    print("Running asynchronous...")
    for i, node in enumerate(g.nodes):
        # reset nodes to s_i^r
        node.val = initial_shared_vals[i]
    async_history = async_consensus(g)

    outfile = "img/comparison.png"

    plot_convergence(
        "Additive secret sharing",
        avg_error(sync_history, true_avg),
        avg_error(async_history, true_avg),
        filename=outfile,
    )

    g.draw()


if __name__ == "__main__":
    main()
