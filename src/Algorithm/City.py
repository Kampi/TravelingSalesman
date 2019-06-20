import numpy

class City(object):
	def __init__(self, x, y, name):
		self.__x = x
		self.__y = y
		self.__name = name

	@property
	def x(self):
		return self.__x
	
	@property
	def y(self):
		return self.__y

	@property
	def name(self):
		return self.__name

	def Distance(self, Neighbor):
		Distance_x = abs(self.__x - Neighbor.x)
		Distance_y = abs(self.__y - Neighbor.y)

		return numpy.sqrt((Distance_x ** 2) + (Distance_y ** 2))

	def __repr__(self):
		return "({}, {}) - {}".format(self.__x, self.__y, self.__name)