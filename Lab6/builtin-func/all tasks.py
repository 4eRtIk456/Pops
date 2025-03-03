import functools, math, time


# 1
def multiply_list(numbers):
    return functools.reduce(lambda x, y: x * y, numbers, 1)

# 2
def count_case(s):
    return {
        "Uppercase": sum(1 for c in s if c.isupper()),
        "Lowercase": sum(1 for c in s if c.islower())
    }

# 3
def is_palindrome(s):
    return s == s[::-1]

# 4
def delayed_sqrt(number, delay):
    time.sleep(delay / 1000)
    return math.sqrt(number)

# 5
def all_true(t):
    return all(t)
