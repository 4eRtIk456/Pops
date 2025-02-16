class String():

    def __init__ (self):
        self.a = ""

    def getString(self):
        self.a = input()

    def printString(self):
        print(self.a.upper())

b=String()
b.getString()
b.printString()