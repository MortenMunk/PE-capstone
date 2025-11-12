class Node:
    def __init__(self, id, val=0.0):
        self.id = id
        self.val = val
        self.initial_val = val
        self.neighbors = set()

        self.initial_s = 0
        self.r_mask = 0
        self.s_shared = 0
