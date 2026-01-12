import numpy as np


def apply_differential_privacy(graph, epsilon=1.0, distribution="laplace"):
    sensitivity = 60  # Range of possible values (age 80 - age 20)

    for node in graph.nodes:
        if distribution == "laplace":
            noise = np.random.laplace(0, sensitivity / epsilon)
        elif distribution == "gaussian":
            noise = np.random.normal(0, sensitivity / epsilon)
        elif distribution == "uniform":  # Added for Bonus 2
            noise = np.random.uniform(-(sensitivity / epsilon), (sensitivity / epsilon))
        else:
            noise = 0
        node.val = node.initial_val + noise
