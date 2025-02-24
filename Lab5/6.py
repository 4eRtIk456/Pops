import re

text = input("Введите строку: ")
result = re.sub(r'[ ,.]', ':', text)
print(result)
