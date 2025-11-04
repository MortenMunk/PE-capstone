class Node:
    def __init__(self, id, val=0.0):
        self.id = id
        self.val = val
        self.neighbors = set()
