def CelToFar(f):
    c = (5 / 9) * (f - 32)
    return c

f = int(input("Enter tempreature in Fahrenheit: "))
print("Tempreature in Centigrade: ", CelToFar(f))
