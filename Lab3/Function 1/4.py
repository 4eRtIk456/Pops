def filter_prime(numbers):
    return [num for num in numbers if num > 1 and all(num % i != 0 for i in range(2, int(num ** 0.5) + 1))]

numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))
prime_numbers = filter_prime(numbers)
print("Prime numbers:", prime_numbers)