import matplotlib.pyplot as plt
import numpy as np
import random


def set_seed(x: int = 42):
    random.seed(x)
    np.random.seed(x)


def plot_convergence(title, history, true_avg, filename="img/convergence.png"):
    errors = [np.mean([(v - true_avg) ** 2 for v in vals]) for vals in history]

    plt.figure()
    plt.plot(errors)
    plt.yscale("log")
    plt.xlabel("iteration")
    plt.ylabel("MSE")
    plt.title(str(title))
    plt.grid(True)
    plt.savefig(filename, bbox_inches="tight")
