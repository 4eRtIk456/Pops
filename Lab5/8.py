import re

text = input("Введите строку: ")
matches = re.findall(r'[A-Z][a-z]*', text)
print(matches)
