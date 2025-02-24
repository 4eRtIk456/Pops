text = input("Введите snake_case строку: ")
words = text.split('_')
result = words[0] + ''.join(word.capitalize() for word in words[1:])
print(result)
