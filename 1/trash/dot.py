# This code is contributed by Ansh Riyal
#https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
#https://stackoverflow.com/questions/3252194/numpy-and-line-intersections

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def onSegment(p, q, r):
	if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
		(q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
		return True
	return False

def orientation(p, q, r):
	
	val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
	if (val > 0):  return 1
	elif (val < 0):  return 2
	else:  return 0

def doIntersect(p1,q1,p2,q2):
	o1 = orientation(p1, q1, p2)
	o2 = orientation(p1, q1, q2)
	o3 = orientation(p2, q2, p1)
	o4 = orientation(p2, q2, q1)

	if ((o1 != o2) and (o3 != o4)): return True
	if ((o1 == 0) and onSegment(p1, p2, q1)): return True
	if ((o2 == 0) and onSegment(p1, q2, q1)): return True
	if ((o3 == 0) and onSegment(p2, p1, q2)): return True
	if ((o4 == 0) and onSegment(p2, q1, q2)): return True
	return False
import numpy as np

def get_intersect(a1, a2, b1, b2):

    s = np.vstack([a1,a2,b1,b2])        
    h = np.hstack((s, np.ones((4, 1)))) 
    l1 = np.cross(h[0], h[1])           
    l2 = np.cross(h[2], h[3])          
    x, y, z = np.cross(l1, l2)          
    if z == 0:                          
        return (float('inf'), float('inf'))
    return (x/z, y/z)

p1 = Point(0, 0)
q1 = Point(10, 10)
p2 = Point(1, 0)
q2 = Point(0, 1)

if doIntersect(p1, q1, p2, q2):
	print("Yes")
	print(get_intersect((0, 0), (10, 10), (1, 0), (0, 1)) )
else:
	print("No")

