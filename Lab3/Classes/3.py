import math

class Point:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def show(self):
        print(f"x = {self.x}, y = {self.y}")

    def move(self, newX, newY):
        self.x = newX
        self.y = newY
    
    def dist(self, other):
        return math.sqrt((self.x - self.y)**2 + (other.x - other.y)**2)

a = Point(2,-4)
b = Point(-5,6)

a.show()
a.move(1,3)
a.show()
print(a.dist(b))


        