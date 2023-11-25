import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize

with open('res.txt') as f:
    lines = f.readlines()

x=[]
y=[]
vals=[]
d=float(lines[0])
for i in range(1,len(lines)):
    x_t1, y_t1, val = lines[i].split()
    x.append(float(x_t1))
    y.append(float(y_t1))
    vals.append(float(val))

cmap = cm.get_cmap('jet')
norm = Normalize(vmin=min(vals), vmax=max(vals))
colors = cmap(norm(vals))

fig=plt.figure()
ax=fig.add_subplot(111, projection='3d')
ax.bar3d(x, y, np.zeros_like(x), d, d, vals, shade=True, color=colors)
#ax.set_zlim(0,0.001)
plt.show()
