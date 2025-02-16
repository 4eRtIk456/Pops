a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)



print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

a = "Hello"
print(a)


"""
Slicing Strings
"""

b = "Hello, World!"
print(b[2:5])
print(b[:5])
print(b[2:])
print(b[-5:-2])


"""
Modify Strings
"""

a = "Hello, World!"
print(a.upper())
print(a.lower())
print(a.strip()) # returns "Hello, World!"
print(a.replace("H", "J"))
print(a.split(",")) # returns ['Hello', ' World!']

"""
Concatenate Strings
"""

a = "Hello"
b = "World"
c = a + b
print(c)
c = a + " " + b
print(c)


"""
Format Strings
"""

age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt = f"The price is {price} dollars"
print(txt)

price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)


"""
Escape Characters
"""

txt = "We are the so-called \"Vikings\" from the north."
print(txt)
txt = 'It\'s alright.'
print(txt) 
txt = "This will insert one \\ (backslash)."
print(txt)  
txt = "Hello\nWorld!"
print(txt) 
txt = "Hello\rWorld!"
print(txt) 
txt = "Hello\tWorld!"
print(txt) 
#This example erases one character (backspace):
txt = "Hello \bWorld!"
print(txt) 
#A backslash followed by three integers will result in a octal value:
txt = "\110\145\154\154\157"
print(txt) 
#A backslash followed by an 'x' and a hex number represents a hex value:
txt = "\x48\x65\x6c\x6c\x6f"
print(txt) 