import argparse
import numpy as np
import random

random.seed(42)
np.random.seed(42)

from src.consensus import async_consensus, sync_consensus
from src.graph import Graph
from src.privacy import apply_differential_privacy
from src.secret_sharing import additive_secret_share_matrix
from src.utils import avg_error, plot_dp_comparison, plot_convergence, avg_error


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
    parser.add_argument("--mode", type=str, default="secret", choices=["secret", "dp"])
    args = parser.parse_args()

    g = Graph(num_nodes=args.nodes, topology=args.top)
    g.assign_initial_values(20, 80)
    true_avg = np.mean([n.initial_val for n in g.nodes])

    if args.mode == "secret":
        additive_secret_share_matrix(g)
        shared_vals = np.array([n.val for n in g.nodes])

        print("Running Secret Sharing (Sync)...")
        sync_history = sync_consensus(g)

        for i, node in enumerate(g.nodes):
            node.val = shared_vals[i]

        print("Running Secret Sharing (Async)...")
        async_history = async_consensus(g)

        plot_convergence(
            "Additive secret sharing",
            avg_error(sync_history, true_avg),
            avg_error(async_history, true_avg),
            filename="img/comparison.png",
        )
    else:
        # --- DP MODE: ASS vs Multiple DP Distributions ---
        # 1. Baseline: Additive Secret Sharing
        for node in g.nodes:
            node.val = node.initial_val  # Reset
        additive_secret_share_matrix(g)
        ass_history = sync_consensus(g)

        # 2. DP: Laplace
        for node in g.nodes:
            node.val = node.initial_val  # Reset
        apply_differential_privacy(g, epsilon=1.0, distribution="laplace")
        laplace_history = sync_consensus(g)

        # 3. DP: Gaussian
        for node in g.nodes:
            node.val = node.initial_val  # Reset
        apply_differential_privacy(g, epsilon=1.0, distribution="gaussian")
        gaussian_history = sync_consensus(g)

        # 4. DP: Uniform
        for node in g.nodes:
            node.val = node.initial_val
        apply_differential_privacy(g, epsilon=1.0, distribution="uniform")
        uniform_history = sync_consensus(g)
        print("Plotting comparison with Laplace, Uniform and Gaussian lines...")
        plot_dp_comparison(
            "Additive vs Laplace vs Gaussian vs Uniform",
            avg_error(ass_history, true_avg),
            avg_error(laplace_history, true_avg),
            avg_error(gaussian_history, true_avg),
            avg_error(uniform_history, true_avg),
            filename="img/dp_detailed_comparison.png",
        )

    g.draw()


if __name__ == "__main__":
    main()
