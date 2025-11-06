import argparse
import numpy as np
import random

random.seed(42)
np.random.seed(42)

from src.consensus import async_consensus, sync_consensus
from src.graph import Graph
from src.secret_sharing import additive_secret_share_matrix
from src.utils import plot_convergence, set_seed


def main():
    # set_seed(42)
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
    parser.add_argument(
        "--mode",
        type=str,
        default="sync",
        help="Consensus mode (sync or async)",
        choices=["sync", "async"],
    )
    args = parser.parse_args()

    g = Graph(num_nodes=args.nodes, topology=args.top)
    g.assign_initial_values(20, 80)
    additive_secret_share_matrix(g)

    true_avg = np.mean([n.val for n in g.nodes])

    if args.mode == "sync":
        history = sync_consensus(g)
        outfile = "img/convergence_sync.png"
        plot_convergence("sync consensus converg.", history, true_avg, filename=outfile)
    else:
        history = async_consensus(g)
        outfile = "img/convergence_async.png"
        plot_convergence(
            "async consensus converg.", history, true_avg, filename=outfile
        )

    g.draw()


if __name__ == "__main__":
    main()
