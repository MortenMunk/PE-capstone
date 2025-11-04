from src.node import Node
import networkx as nx
import matplotlib.pyplot as plt
import random
import math


class Graph:
    def __init__(self, num_nodes=0, topology=None):
        self.nodes = [Node(id=i) for i in range(num_nodes)]
        self.topology = topology
        self._connect_nodes()

    def _connect_nodes(self):
        if len(self.nodes) < 2:
            return

        match self.topology:
            case "mesh":
                self._random_mesh()
            case "ring":
                n = len(self.nodes)
                for i in range(n):
                    a = self.nodes[i]
                    b = self.nodes[(i + 1) % n]
                    self._connect(a, b)
            case "star":
                center = self.nodes[0]
                for node in self.nodes[1:]:
                    self._connect(center, node)
            case "full":
                for i, a in enumerate(self.nodes):
                    for b in self.nodes[i + 1 :]:
                        self._connect(a, b)
            case _:
                raise ValueError(f"Topology: {self.topology} is not valid")

    def _random_mesh(self):
        n = len(self.nodes)
        if n < 2:
            return

        base_prob = 1 / math.log(n + 2)
        p = min(0.8, max(0.02, base_prob))
        for i, a in enumerate(self.nodes):
            for b in self.nodes[i + 1 :]:
                if random.random() < p:
                    self._connect(a, b)

    def _connect(self, a: Node, b: Node):
        a.neighbors.add(b)
        b.neighbors.add(a)

    def draw(self):
        G = nx.Graph()
        for node in self.nodes:
            for neighbor in node.neighbors:
                G.add_edge(node.id, neighbor.id)
        nx.draw(
            G,
            with_labels=True,
            node_color="lightblue",
            node_size=800,
            font_weight="bold",
        )
        plt.savefig("img/graph.png", bbox_inches="tight")
