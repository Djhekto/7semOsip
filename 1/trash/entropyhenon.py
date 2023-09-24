# gpt derived from https://github.com/ambron60/henon-attractor

#https://www.sciencedirect.com/science/article/pii/S0960077912000586

import numpy as np
from scipy.spatial import distance

def henon_map(x, y, a=1.4, b=0.3):
    return y + 1 - a * x**2, b * x

def entropy_henon(x, y, n=10000):
    points = np.zeros((n, 2))
    for i in range(n):
        points[i] = x, y
        x, y = henon_map(x, y)
    
    # Calculate pairwise distances between points
    pairwise_distances = distance.pdist(points)
    
    # Calculate histogram of distances
    hist, _ = np.histogram(pairwise_distances, bins='auto', density=True)
    
    # Calculate entropy
    entropy = -np.sum(hist * np.log2(hist))
    
    return entropy

# Example usage
x0 = 0.1
y0 = 0.1
entropy = entropy_henon(x0, y0)
print("Entropy of Henon attractor: ", entropy)
