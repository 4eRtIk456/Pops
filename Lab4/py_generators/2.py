def evenNumbers(n):
    for i in range(0, n+1, 2):
        yield str(i)

n = int(input("Введите число: "))
evenNum = evenNumbers(n)
print(", ".join(evenNum))