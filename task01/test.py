from task01 import count, abc, abc_stog, rjesenja, Point2D, Polar2D
import math


if __name__ == "__main__":

    def paran(b):
        return b % 2 == 0

    # a1
    print(count([2, 4, 5, 3, 7, 6], paran))
    # a2
    print(abc(4, ""))
    # a3
    print(abc_stog(4))
    # a4
    rjesenja([23, 10, 15, 13], [])
    # b
    p1 = Point2D(1, 1)
    p2 = Polar2D(math.pi / 4, 2**0.5)
    print(p1, p2)
    print(p1.polar(), p2.kart())
    print(p1 == p2, p2 == p1)
    print(p1 != p2, p2 != p1)
    print(p1 + p2, p2 + p1)
    print(p1.udaljenost(), p2.udaljenost())
