import matplotlib.pyplot as plt
import numpy as np
import random


def set_seed(x: int = 42):
    random.seed(x)
    np.random.seed(x)


def plot_dp_comparison(
    title, ass_err, laplace_err, gaussian_err, uniform_err, filename="img/dp"
):
    plt.figure(figsize=(10, 6))
    plt.plot(ass_err, label="Secret Sharing (ASS)", color="blue", linewidth=2)
    plt.plot(laplace_err, label="DP: Laplace", color="red", linestyle="--")
    plt.plot(gaussian_err, label="DP: Gaussian", color="green", linestyle="--")
    plt.plot(uniform_err, label="DP: Uniform", color="purple", linestyle="--")

    plt.yscale("log")
    plt.xlabel("Iteration")
    plt.ylabel("Max Error (log)")
    plt.title(title)
    # plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


def plot_convergence(title, line1_errors, line2_errors, filename="img/comparison.png"):
    plt.figure(figsize=(10, 6))

    if "Differential" in title:
        label1, label2 = "Secret Sharing (ASS)", "Differential Privacy (DP)"
    else:
        label1, label2 = "Synchronous Consensus", "Asynchronous Consensus"

    plt.plot(line1_errors, label=label1)
    plt.plot(line2_errors, label=label2)

    plt.yscale("log")
    plt.xlabel("Iteration")
    plt.ylabel("Max error (log)")
    plt.title(title)
    # plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend()
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


def avg_error(history, true_avg):
    errors = []
    for vals in history:
        vals = np.array(vals)
        max_err = np.max(np.abs(vals - true_avg))
        errors.append(max_err)
    return errors
