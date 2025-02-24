import re

text = input("Введите CamelCase строку: ")
result = re.sub(r'([A-Z])', r'_\1', text).lower().lstrip('_')
print(result)
