import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np



N = 11
M = 11
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, M)









# Create an application instance
app = pg.mkQApp()

# Create a 3D widget
view = gl.GLViewWidget()
view.show()

# Create three grids
xgrid = gl.GLGridItem()
ygrid = gl.GLGridItem()
zgrid = gl.GLGridItem()

# Add the grids to the widget
view.addItem(xgrid)
view.addItem(ygrid)
view.addItem(zgrid)

# Rotate x and y grids to face the correct direction
xgrid.rotate(90, 0, 1, 0)
ygrid.rotate(90, 1, 0, 0)

"""
for i in range(5):
    glvw = gl.GLViewWidget()
    z = np.random.random((N, M))
    surf = gl.GLSurfacePlotItem(x=x, y=y, z=z)
    glvw.addItem(surf)
    layoutgb.addWidget(glvw, 0, i)
"""
# Run the application
app.exec()
