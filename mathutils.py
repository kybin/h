def lineIntersectionPoint((x1, y1, x2, y2), (x3, y3, x4, y4)):
	'''	find intersection point with given 2 lines (4 points)
		L1 = ((x1,y1), (x2,y2))
		L2 = ((x3,y3), (x4,y4))
		http://en.wikipedia.org/wiki/Line-line_intersection
	'''
	x = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
	y = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
	return x, y

