import math


# a1
def count(lst, predicate):
    if not lst:
        return 0
    return count(lst[1:], predicate) + predicate(lst[0])


# a2
def abc(length, partial=""):
    if length == 0:
        return [partial]
    combinations = []
    for char in "ABC":
        combinations += abc(length - 1, partial + char)
    return combinations


# a3
def abc_stog(lenght):
    if lenght == 0:
        return
    stack = [""]
    combinations = []
    while stack:
        partial = stack.pop()
        if len(partial) == lenght:
            combinations.append(partial)
        else:
            for char in "ABC":
                stack.append(partial + char)
    return combinations


# a4
# def rjesenja(lst, currentLst=[]):
#     def isDivisible(numbers):
#         return sum(numbers) ** 2 % 23 == 0
#     # print(currentLst)
#     if isDivisible(currentLst) and len(currentLst) > 0:
#         print(currentLst)
#     for i in range(len(lst)):
#         rjesenja(lst[i + 1 :], currentLst + [lst[i]])


def rjesenja(lista, currentLst=[]):
    if currentLst:
        if sum(currentLst) % 23 == 0:
            print(currentLst)
    if not lista:
        return
    rjesenja(lista[1:], currentLst)
    rjesenja(lista[1:], currentLst + [lista[0]])


# b
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def polar(self):
        angle = math.atan2(self.y, self.x)
        magnitude = (self.x**2 + self.y**2) ** 0.5
        return Polar2D(angle, magnitude)

    def __repr__(self):
        return f"Point2D =>({self.x}, {self.y})"

    def __neg__(self):
        return Point2D(-self.x, -self.y)

    def __add__(self, other):
        other = other.kart()
        return Point2D(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        other = other.kart()
        return abs(self.x - other.x) < 0.01 and abs(self.y - other.y) < 0.01

    def __ne__(self, other):
        return not self == other

    def udaljenost(self):
        return (self.x**2 + self.y**2) ** 0.5


class Polar2D:
    def __init__(self, angle, magnitude):
        self.angle = angle
        self.magnitude = magnitude

    def kart(self):
        x = math.cos(self.angle) * self.magnitude
        y = math.sin(self.angle) * self.magnitude
        return Point2D(x, y)

    def __repr__(self):
        return f"Polar2D({self.angle}, {self.magnitude})"

    def __neg__(self):
        return Polar2D(self.angle + math.pi, self.magnitude)

    def __add__(self, other):
        other = other.polar()
        x = (
            math.cos(self.angle) * self.magnitude
            + math.cos(other.angle) * other.magnitude
        )
        y = (
            math.sin(self.angle) * self.magnitude
            + math.sin(other.angle) * other.magnitude
        )
        return Point2D(x, y).polar()

    def __eq__(self, other):
        other = other.polar()
        return (
            abs(self.angle - other.angle) < 0.01
            and abs(self.magnitude - other.magnitude) < 0.01
        )

    def __ne__(self, other):
        return not self == other

    def udaljenost(self):
        return self.magnitude
