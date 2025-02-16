
def unique_elements(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)
    return unique_lst

num = list(map(int, input("Enter numbers separated by spaces: ").split()))
print(unique_elements(num))
