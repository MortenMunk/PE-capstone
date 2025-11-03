from node import Node


class Graph:
    def __init__(self, num_nodes=0, topology=None):
        self.nodes = [Node(id=i) for i in range(num_nodes)]
        self.topology = topology
        self._connect_nodes()

    def _connect_nodes(self):
        pass

    def _connect(self, a: Node, b: Node):
        a.neighbors.add(b)
        b.neighbors.add(a)
