def divisible(n):
    for i in range(n+1):
        if (i%3 == 0 and i%4 == 0):
            yield str(i)

n = int(input("Введите число: "))
div = divisible(n)
print(", ".join(div))