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

        if not self.is_connected():
            G = nx.Graph()
            for node in self.nodes:
                for neighbor in node.neighbors:
                    G.add_edge(node.id, neighbor.id)

            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                a = random.choice(list(components[i]))
                b = random.choice(list(components[i + 1]))
                self._connect(self.nodes[a], self.nodes[b])

    def _connect(self, a: Node, b: Node):
        a.neighbors.add(b)
        b.neighbors.add(a)

    def draw(self):
        G = nx.Graph()
        for node in self.nodes:
            for neighbor in node.neighbors:
                G.add_edge(node.id, neighbor.id)

        pos = nx.spring_layout(G, seed=42)
        labels = {
            node.id: f"{node.initial_val:.1f} -> {node.val:.1f}" for node in self.nodes
        }

        plt.figure(figsize=(6, 6))
        nx.draw(
            G,
            pos,
            with_labels=True,
            labels=labels,
            node_color="lightblue",
            node_size=1200,
            font_weight="bold",
            font_size=10,
        )
        plt.title(f"{self.topology} topology")
        plt.savefig("img/graph.png", bbox_inches="tight")
        plt.close()

    def is_connected(self):
        G = nx.Graph()
        for node in self.nodes:
            for neighbor in node.neighbors:
                G.add_edge(node.id, neighbor.id)
        return nx.is_connected(G)

    def assign_initial_values(self, low=10, high=100):
        for node in self.nodes:
            node.val = random.uniform(low, high)
            node.initial_val = node.val
