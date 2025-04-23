from contextlib import contextmanager
import time
import sys

# Basic Exception Handling
print("\n=== Basic Exception Handling ===")
try:
    age = int(input("Enter your age: "))
except ValueError as e:
    print("You didn't enter a valid integer")
    print(f"Error details: {e}")


# Handling Different Exceptions
print("\n=== Handling Different Exceptions ===")


def divide(a, b):
    try:
        result = a / b
        numbers = [1, 2, 3]
        print(numbers[result])  # Potential IndexError
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except IndexError:
        print("Index out of range!")
        return None
    except Exception as e:
        print(f"Something went wrong: {e}")
        return None


print(divide(10, 0))  # ZeroDivisionError
print(divide(10, 5))  # IndexError (trying to access index 2.0)


# Cleaning Up with Finally
print("\n=== Cleaning Up with Finally ===")


def open_file(filename):
    try:
        file = open(filename, "r")
        content = file.read()
        return content
    except FileNotFoundError:
        print(f"Sorry, the file {filename} does not exist")
        return None
    finally:
        print("Cleanup: Ensuring file is closed")
        try:
            file.close()
        except NameError:  # file was never opened
            pass


open_file("nonexistent.txt")


# The With Statement (Context Managers)
print("\n=== The With Statement ===")


# Custom context manager
@contextmanager
def timer():
    start = time.time()
    yield
    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")


# Using the custom context manager
with timer():
    # Simulate some work
    time.sleep(1)
    print("Work completed!")


# Custom File Context Manager
class FileManager:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        try:
            self.file = open(self.filename, "r")
            return self.file
        except FileNotFoundError:
            print(f"File {self.filename} not found")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
            print(f"File {self.filename} closed")
        return True  # Suppress any exceptions


# Using custom context manager
with FileManager("test.txt") as file:
    if file:
        print("File opened successfully")


# Raising Exceptions
print("\n=== Raising Exceptions ===")


class AgeError(Exception):
    """Exception raised for invalid age values."""

    def __init__(self, age, message="Invalid age provided"):
        self.age = age
        self.message = message
        super().__init__(self.message)


def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0:
        raise AgeError(age, "Age cannot be negative")
    if age > 150:
        raise AgeError(age, "Age is unrealistically high")
    return True


# Testing custom exceptions
try:
    validate_age(-5)
except AgeError as e:
    print(f"AgeError: {e.message} (value: {e.age})")
except TypeError as e:
    print(f"TypeError: {e}")


# Cost of Raising Exceptions
print("\n=== Cost of Raising Exceptions ===")


def divide_with_try_except(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def divide_with_if(a, b):
    if b == 0:
        return None
    return a / b


# Performance comparison
def measure_performance(func, iterations=1000000):
    start = time.time()
    for _ in range(iterations):
        func(10, 2)  # Normal case
        func(10, 0)  # Exception case
    end = time.time()
    return end - start


print("\nPerformance Test:")
try_except_time = measure_performance(divide_with_try_except)
if_time = measure_performance(divide_with_if)

print(f"Try-Except approach: {try_except_time:.2f} seconds")
print(f"If-condition approach: {if_time:.2f} seconds")
print(f"Try-Except is {try_except_time/if_time:.2f}x slower")

# Example of proper exception handling in real-world scenario
print("\n=== Real-world Exception Handling Example ===")


def process_user_data(user_id):
    try:
        # Simulate database operations
        if not isinstance(user_id, int):
            raise TypeError("User ID must be an integer")

        if user_id < 0:
            raise ValueError("User ID cannot be negative")

        # Simulate some processing
        print(f"Processing user data for ID: {user_id}")

    except TypeError as e:
        print(f"Type Error: {e}")
        # Log error, notify admin, etc.
    except ValueError as e:
        print(f"Value Error: {e}")
        # Log error, notify user, etc.
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Log error, notify admin, rollback changes, etc.
    else:
        print("Processing completed successfully!")
        # Commit changes, notify user, etc.
    finally:
        print("Cleanup operations completed")
        # Close connections, free resources, etc.


process_user_data(123)  # Valid case
process_user_data(-1)  # Invalid case
process_user_data("abc")  # Invalid type
