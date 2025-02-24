import re

text = input("Введите строку: ")
result = re.sub(r'([A-Z])', r' \1', text).strip()
print(result)
