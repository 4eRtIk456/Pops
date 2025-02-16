from itertools import permutations

def print_permutations(s):
    for perm in permutations(s):
        print("".join(perm))

s = input("Enter a string: ")
print_permutations(s)