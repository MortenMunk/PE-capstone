import argparse
from src.graph import Graph


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
    g.draw()


if __name__ == "__main__":
    main()
