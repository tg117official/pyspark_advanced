# Exercise 1: Calculate Factorial Recursively
# Problem Statement: Write a recursive function to calculate the factorial of a number.
# Use pdb to debug and step through the recursive calls.

def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

if __name__ == "__main__":
    import pdb
    pdb.set_trace()  # Debugger starts here
    num = 5
    print(f"Factorial of {num} is {factorial(num)}")

# Exercise 2: Find the Sum of Elements in a List
# Problem Statement: Write a function to find the sum of all elements in a list.
# Use pdb to debug the iteration and summation process.

def sum_of_list(lst):
    total = 0
    for num in lst:
        total += num
    return total

if __name__ == "__main__":
    import pdb
    pdb.set_trace()  # Debugger starts here
    numbers = [1, 2, 3, 4, 5]
    print(f"Sum of list {numbers} is {sum_of_list(numbers)}")

# Exercise 3: Reverse a String
# Problem Statement: Write a function to reverse a given string.
# Use pdb to debug the process of reversing.

def reverse_string(s):
    reversed_str = "".join(reversed(s))
    return reversed_str

if __name__ == "__main__":
    import pdb
    pdb.set_trace()  # Debugger starts here
    input_str = "hello"
    print(f"Reversed string of '{input_str}' is '{reverse_string(input_str)}'")

# Exercise 4: Check Palindrome
# Problem Statement: Write a function to check if a given string is a palindrome.
# Use pdb to debug the comparison process.

def is_palindrome(s):
    return s == s[::-1]

if __name__ == "__main__":
    import pdb
    pdb.set_trace()  # Debugger starts here
    test_str = "madam"
    print(f"Is '{test_str}' a palindrome? {is_palindrome(test_str)}")

# Exercise 5: Find Prime Numbers in a Range
# Problem Statement: Write a function to find all prime numbers in a given range.
# Use pdb to debug the process of checking for primes.

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def primes_in_range(start, end):
    primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
    return primes

if __name__ == "__main__":
    import pdb
    pdb.set_trace()  # Debugger starts here
    start_range, end_range = 10, 50
    print(f"Prime numbers between {start_range} and {end_range}: {primes_in_range(start_range, end_range)}")