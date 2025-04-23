from collections import deque
from array import array
from typing import List, Dict, Set, Tuple
import heapq

# Lists
print("\n=== Lists ===")
numbers = [1, 2, 3, 4, 5]
print("Original list:", numbers)

# Accessing Items
print("\n=== Accessing Items ===")
print("First item:", numbers[0])
print("Last item:", numbers[-1])
print("Slice:", numbers[1:4])

# List Unpacking
print("\n=== List Unpacking ===")
first, second, *others = numbers
print("First:", first)
print("Second:", second)
print("Others:", others)

# Looping over Lists
print("\n=== Looping over Lists ===")
for index, number in enumerate(numbers):
    print(f"Index: {index}, Value: {number}")

# Adding or Removing Items
print("\n=== Adding or Removing Items ===")
numbers.append(6)
numbers.insert(0, 0)
numbers.remove(3)
last = numbers.pop()
print("Modified list:", numbers)

# Finding Items
print("\n=== Finding Items ===")
print("Index of 4:", numbers.index(4))
print("Count of 1:", numbers.count(2))

# Sorting Lists
print("\n=== Sorting Lists ===")
unordered = [4, 2, 7, 1, 9]
print("Sorted:", sorted(unordered))
print("Original:", unordered)
unordered.sort(reverse=True)
print("Reverse sorted:", unordered)

# Lambda Functions
print("\n=== Lambda Functions ===")
points = [(1, 2), (3, 1), (2, 4)]
points.sort(key=lambda point: point[1])
print("Sorted by y-coordinate:", points)

# Map Function
print("\n=== Map Function ===")
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print("Squared numbers:", squared)

# Filter Function
print("\n=== Filter Function ===")
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

# List Comprehensions
print("\n=== List Comprehensions ===")
squares = [x**2 for x in range(5)]
print("Squares:", squares)
even_squares = [x**2 for x in range(5) if x % 2 == 0]
print("Even squares:", even_squares)

# Zip Function
print("\n=== Zip Function ===")
list1 = [1, 2, 3]
list2 = ["a", "b", "c"]
zipped = list(zip(list1, list2))
print("Zipped lists:", zipped)

# Stacks
print("\n=== Stacks ===")
stack = []
stack.append(1)  # push
stack.append(2)
stack.append(3)
print("Stack:", stack)
print("Popped:", stack.pop())  # pop
print("Stack after pop:", stack)

# Queues
print("\n=== Queues ===")
queue = deque()
queue.append(1)  # enqueue
queue.append(2)
queue.append(3)
print("Queue:", queue)
print("Dequeued:", queue.popleft())  # dequeue
print("Queue after dequeue:", queue)

# Tuples
print("\n=== Tuples ===")
coordinates = (1, 2, 3)
print("Coordinates:", coordinates)
x, y, z = coordinates  # tuple unpacking
print(f"x: {x}, y: {y}, z: {z}")

# Swapping Variables
print("\n=== Swapping Variables ===")
a, b = 1, 2
print(f"Before swap: a = {a}, b = {b}")
a, b = b, a
print(f"After swap: a = {a}, b = {b}")

# Arrays
print("\n=== Arrays ===")
numbers_array = array("i", [1, 2, 3, 4, 5])
print("Array:", numbers_array)
numbers_array.append(6)
print("Array after append:", numbers_array)

# Sets
print("\n=== Sets ===")
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
print("Union:", set1 | set2)
print("Intersection:", set1 & set2)
print("Difference:", set1 - set2)

# Dictionaries
print("\n=== Dictionaries ===")
person = {"name": "John", "age": 30, "city": "New York"}
print("Person:", person)
print("Keys:", person.keys())
print("Values:", person.values())
print("Items:", person.items())

# Dictionary Comprehensions
print("\n=== Dictionary Comprehensions ===")
squares_dict = {x: x**2 for x in range(5)}
print("Squares dictionary:", squares_dict)

# Generator Expressions
print("\n=== Generator Expressions ===")
gen = (x**2 for x in range(5))
print("Generator expression:", gen)
print("Generator values:", list(gen))

# Unpacking Operator
print("\n=== Unpacking Operator ===")
numbers = [1, 2, 3]
more_numbers = [*numbers, 4, 5]
print("Unpacked list:", more_numbers)

dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, **dict1}
print("Unpacked dictionary:", dict2)
