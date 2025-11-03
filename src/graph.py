from node import Node


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

    # TODO: def _random_mesh()

    def _connect(self, a: Node, b: Node):
        a.neighbors.add(b)
        b.neighbors.add(a)
