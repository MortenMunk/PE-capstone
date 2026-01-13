import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, laplace, uniform

# 1. Setup the x-axis range
x = np.linspace(-5, 5, 1000)

# 2. Define parameters (using scale=1 for comparison)
mu = 0
scale = 1

# 3. Calculate PDFs using scipy.stats
# Gaussian: Bell-shaped curve
gaussian_pdf = norm.pdf(x, mu, scale)

# Laplace: Sharp peak, heavy tails (standard for DP)
laplace_pdf = laplace.pdf(x, mu, scale)

# Uniform: Flat plateau (standard for additive secret sharing)
# We set the range [-sqrt(3), sqrt(3)] so it has the same variance (1) as the others
u_width = scale * np.sqrt(3)
uniform_pdf = uniform.pdf(x, -u_width, 2 * u_width)

# 4. Create the plot
plt.figure(figsize=(10, 6))
plt.plot(
    x,
    gaussian_pdf,
    label=f"Gaussian",
    color="green",
    linestyle="--",
)
plt.plot(
    x,
    laplace_pdf,
    label=f"Laplace",
    color="red",
    linestyle="--",
)
plt.plot(
    x,
    uniform_pdf,
    label=f"Uniform",
    color="purple",
    linestyle="--",
)

# Formatting
plt.title("Probability Density Functions: Gaussian vs. Laplace vs. Uniform")
plt.xlabel("Value")
plt.ylabel("Probability Density")
plt.grid(True, alpha=0.3)
plt.legend()

# Save the file
plt.savefig("img/distribution_comparison.png", bbox_inches="tight")
plt.close()
