def has_33(a):
    for i in range(len(a) - 1):
        if a[i] == 3 and a[i+1] == 3:
            return True
            break
    return False
    
num = list(map(int, input("Enter numbers separated by spaces: ").split()))
print(has_33(num))