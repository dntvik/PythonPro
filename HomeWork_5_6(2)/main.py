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

    def __contains__(self, point):
        distance = math.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)
        return distance <= self.radius


c1 = Circle(1, 2, 10)
p1 = Point(1, 2)

print(p1 in c1)

p2 = Point(12, 2)
print(p2 in c1)
