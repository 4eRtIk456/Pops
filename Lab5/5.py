import re

text = input("Введите строку: ")
match = bool(re.fullmatch(r'a.*b', text))
print(match)
