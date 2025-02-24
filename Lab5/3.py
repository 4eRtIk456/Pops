import re

text = input("Введите строку: ")
matches = re.findall(r'\b[a-z]+_[a-z]+\b', text)
print(matches)
