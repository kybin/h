import math

def lineIntersectionPoint((x1, y1, x2, y2), (x3, y3, x4, y4)):
	'''	find intersection point with given 2 lines (4 points)
		L1 = (x1,y1,x2,y2)
		L2 = (x3,y3,x4,y4)
		http://en.wikipedia.org/wiki/Line-line_intersection
	'''
	denominator = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
	if not denominator:
		return 0,0
	x = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/denominator
	y = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/denominator
	return x, y

def lineToPointDistance((x1,y1,x2,y2),(x3, y3)):
	dx1, dy1 = x2-x1, y2-y1
	dr1 = math.sqrt(dx1*dx1 + dy1*dy1)
	dx2, dy2 = x3-x1, y3-y1
	dr2 = math.sqrt(dx2*dx2 + dy2*dy2) 

	rad1, rad2 = math.asin(dx1/dr1), math.asin(dx2/dr2)
	rad = rad2-rad1

	dist = math.sin(rad)*dr2
	return abs(dist)


