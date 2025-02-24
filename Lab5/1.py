import re

s = input("Enter a string: ")
result = re.match(r'a*b*', s)
print(result)