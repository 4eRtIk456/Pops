def numDS(n):
    for i in range(n,-1,-1):
        yield i;

n = int(input("Введите число: "))
print(*numDS(n))
