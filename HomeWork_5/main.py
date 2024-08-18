import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, point):
        distance = math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
        return distance <= self.radius
