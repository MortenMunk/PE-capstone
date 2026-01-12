import matplotlib.pyplot as plt
import numpy as np
import random


def set_seed(x: int = 42):
    random.seed(x)
    np.random.seed(x)


def plot_convergence(title, sync_errors, async_errors, filename="img/comparison.png"):
    plt.figure(figsize=(10, 6))
    plt.plot(sync_errors, label="Synchronous Consensus")
    plt.plot(async_errors, label="Asynchronous Consensus")

    plt.yscale("log")
    plt.xlabel("Iteration")
    plt.ylabel("Error")
    plt.title(title)
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


def avg_error(history, true_avg):
    errors = []
    for vals in history:
        vals = np.array(vals)
        mean_abs_error = np.mean(np.abs(vals - true_avg))
        errors.append(mean_abs_error)
    return errors
