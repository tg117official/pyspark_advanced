# Exercise 1: Bug in dictionary key lookup
# Problem: Write a function that returns the value for a given key in a dictionary.
# Bug: The function doesn't handle missing keys properly and raises a KeyError.
# Relevance: Handling missing keys is critical for safe dictionary operations in applications.
def get_dict_value(data, key):
    return data[key]  # Bug: No check for key existence

data = {"name": "Alice", "age": 30}
print("Exercise 1 Result:", get_dict_value(data, "address"))  # Expected: "Key not found", Buggy Output: KeyError

# Exercise 2: Incorrect sorting logic
# Problem: Write a function to sort a list of dictionaries by a given key.
# Bug: The function doesn't handle cases where the key is missing in some dictionaries.
# Relevance: Ensures consistent sorting when data structures may be incomplete.
def sort_by_key(items, key):
    return sorted(items, key=lambda x: x[key])  # Bug: No check for missing key

items = [{"name": "Alice"}, {"name": "Bob"}, {"age": 25}]
print("Exercise 2 Result:", sort_by_key(items, "name"))  # Expected: Sorted list, Buggy Output: KeyError

# Exercise 3: Bug in file reading
# Problem: Write a function to read a file and return its content as a list of lines.
# Bug: The function doesn't handle cases where the file doesn't exist.
# Relevance: Ensures file-handling operations are robust against missing files.
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.readlines()  # Bug: No handling for FileNotFoundError

print("Exercise 3 Result:", read_file("non_existent_file.txt"))  # Expected: "File not found", Buggy Output: FileNotFoundError

# Exercise 4: Bug in recursive function for reversing a string
# Problem: Write a recursive function to reverse a string.
# Bug: The base case is incorrect, leading to infinite recursion.
# Relevance: Proper recursive logic prevents stack overflow and ensures correct results.
def reverse_string(s):
    if len(s) == 0:  # Bug: Incorrect base case; should check for length == 1
        return s
    return reverse_string(s[1:]) + s[0]

print("Exercise 4 Result:", reverse_string("hello"))  # Expected: "olleh", Buggy Output: RecursionError

# Exercise 5: Incorrect handling of duplicates in a list
# Problem: Write a function to remove duplicates from a list while preserving the order.
# Bug: The function removes all occurrences of duplicates instead of keeping the first occurrence.
# Relevance: Preserving data integrity is crucial in deduplication tasks.
def remove_duplicates(items):
    seen = set()
    return [x for x in items if x not in seen and seen.add(x)]  # Bug: Incorrect set handling

print("Exercise 5 Result:", remove_duplicates([1, 2, 2, 3, 1]))  # Expected: [1, 2, 3], Buggy Output: [3]


############################################## Solutions ################################################


# Bugs and Fixes:

# Exercise 1:
# Bug: No handling for missing keys in the dictionary.
# Fix:
# return data.get(key, "Key not found")

# Exercise 2:
# Bug: Missing keys in dictionaries cause KeyError.
# Fix:
# return sorted(items, key=lambda x: x.get(key, ""))


# Exercise 3:
# Bug: No handling for FileNotFoundError.
# Fix:
# try:
#     with open(file_path, "r") as f:
#         return f.readlines()
# except FileNotFoundError:
#     return "File not found"


# Exercise 4:
# Bug: Base case is incorrect, causing infinite recursion.
# Fix:
# if len(s) <= 1:
#     return s


# Exercise 5:
# Bug: The set.add method in the list comprehension always returns None.
# Fix:
# def remove_duplicates(items):
#     seen = set()
#     result = []
#     for x in items:
#         if x not in seen:
#             seen.add(x)
#             result.append(x)
#     return result