# Exercise 1: Incorrect sum calculation
# Problem: Write a function to calculate the sum of a list of numbers.
# Bug: The function only adds even numbers instead of all numbers.
# Relevance: Debugging incorrect logic in basic numerical functions is crucial in financial and data processing applications.
def calculate_sum(numbers):
    return sum(n for n in numbers if n % 2 == 0)  # Bug: Filtering even numbers

print("Exercise 1 Result:", calculate_sum([1, 2, 3, 4, 5]))  # Expected: 15, Buggy Output: 6

# Exercise 2: Division by zero
# Problem: Write a function to calculate the average of a list of numbers.
# Bug: The function doesn't handle empty lists, leading to a division by zero error.
# Relevance: Handling edge cases like empty data is essential in robust applications.
def calculate_average(numbers):
    return sum(numbers) / len(numbers)  # Bug: No check for empty list

print("Exercise 2 Result:", calculate_average([]))  # Expected: Error handling, Buggy Output: ZeroDivisionError

# Exercise 3: IndexError in list access
# Problem: Write a function to return the nth element of a list.
# Bug: The function doesn't check if the index is within the bounds of the list.
# Relevance: Preventing out-of-bound errors is crucial in list-based data structures.
def get_element(lst, index):
    return lst[index]  # Bug: No check for valid index

print("Exercise 3 Result:", get_element([1, 2, 3], 5))  # Expected: Error handling, Buggy Output: IndexError

# Exercise 4: Incorrect string capitalization
# Problem: Write a function to capitalize the first letter of every word in a string.
# Bug: The function capitalizes every character instead of just the first letter of each word.
# Relevance: Ensuring proper string formatting is important in text-based applications.
def capitalize_words(sentence):
    return sentence.upper()  # Bug: Converts entire string to uppercase

print("Exercise 4 Result:", capitalize_words("hello world"))  # Expected: "Hello World", Buggy Output: "HELLO WORLD"

# Exercise 5: Infinite loop in factorial calculation
# Problem: Write a function to calculate the factorial of a number.
# Bug: The recursive function doesn't have a proper base case, causing an infinite loop.
# Relevance: Handling recursion correctly is crucial to avoid performance and memory issues.
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n)  # Bug: Missing n-1 in recursive call

print("Exercise 5 Result:", factorial(5))  # Expected: 120, Buggy Output: RecursionError


####################################################### Explanation ########################################

# Bugs and Fixes:

# Exercise 1:
# Bug: The function filters even numbers.
# Fix: Remove the condition to include all numbers:
# return sum(numbers)

# Exercise 2:
# Bug: Division by zero for empty lists.
# Fix: Add a condition to handle empty lists:
# if not numbers:
#     return 0  # or raise ValueError("List is empty")

# Exercise 3:
# Bug: No index validation, causing IndexError.
# Fix: Check if the index is within bounds:
# if index < 0 or index >= len(lst):
#     raise IndexError("Index out of bounds")

# Exercise 4:
# Bug: Converts the entire string to uppercase instead of capitalizing words.
# Fix: Use str.title() or capitalize each word:
# return " ".join(word.capitalize() for word in sentence.split())

# Exercise 5:
# Bug: Missing base case decrement (n - 1).
# Fix: Modify the recursive call:
# return n * factorial(n - 1)