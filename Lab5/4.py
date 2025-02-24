import re

text = input("Введите строку: ")
matches = re.findall(r'\b[A-Z][a-z]+\b', text)
print(matches)
