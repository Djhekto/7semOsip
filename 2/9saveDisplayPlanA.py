import numpy as np
import matplotlib.pyplot as plt

# Example using savefig()
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.savefig('plot.png')

# Example using imsave()
image = np.random.randn(100, 100)
plt.imsave('plot.png', image)