def histogram(lst):
    for num in lst:
        print('*' * num)

num = list(map(int, input("Enter numbers separated by spaces: ").split()))
print(histogram(num))
