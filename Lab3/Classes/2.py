class Shape:

    def __init__(self):
        pass

    def area(self):
        return 0
    
class Square(Shape):

    def __init__(self, length):
        super().__init__()
        self.length = length

    def area(self):
        return self.length*self.length
    
a=Square(5)
print(a.area())

class Rectangle(Shape):

    def __init__(self, length, width):
        super().__init__()
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width
    
b=Rectangle(3,4)
print(b.area())
