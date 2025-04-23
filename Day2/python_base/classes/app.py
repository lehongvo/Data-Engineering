from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any
import math

# Basic Class Creation
print("\n=== Basic Class Creation ===")


class Point:
    # Class attribute
    default_color = "red"

    # Constructor
    def __init__(self, x: float, y: float):
        # Instance attributes
        self.x = x
        self.y = y

    # Instance method
    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    # Class method
    @classmethod
    def zero(cls):
        return cls(0, 0)

    # Static method
    @staticmethod
    def calculate_distance(p1, p2):
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


# Creating instances
p1 = Point(1, 2)
# move
p1.move(1, 2)
p2 = Point.zero()
print(f"p1: ({p1.x}, {p1.y})")
print(f"p2: ({p2.x}, {p2.y})")
print(f"Distance: {Point.calculate_distance(p1, p2):.2f}")


# Magic Methods and Operator Overloading
print("\n=== Magic Methods and Operator Overloading ===")


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"


v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 * 2 = {v1 * 2}")


# Custom Container
print("\n=== Custom Container ===")


class TagCloud:
    def __init__(self):
        self.__tags = {}

    def add(self, tag: str):
        self.__tags[tag.lower()] = self.__tags.get(tag.lower(), 0) + 1

    def __getitem__(self, tag: str):
        return self.__tags.get(tag.lower(), 0)

    def __setitem__(self, tag: str, count: int):
        self.__tags[tag.lower()] = count

    def __len__(self):
        return len(self.__tags)

    def __iter__(self):
        return iter(self.__tags)


cloud = TagCloud()
cloud.add("Python")
cloud.add("python")
cloud.add("java")
print(f"Python count: {cloud['python']}")


# Properties
print("\n=== Properties ===")


class Circle:
    def __init__(self, radius):
        self.__radius = radius

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self.__radius = value

    @property
    def area(self):
        return math.pi * self.__radius**2


circle = Circle(5)
print(f"Circle area: {circle.area:.2f}")
try:
    circle.radius = -1
except ValueError as e:
    print(f"Error: {e}")


# Inheritance and Method Overriding
print("\n=== Inheritance and Method Overriding ===")


class Animal:
    def __init__(self, name: str):
        self.name = name

    def make_sound(self):
        pass


class Dog(Animal):
    def make_sound(self):
        return "Woof!"


class Cat(Animal):
    def make_sound(self):
        return "Meow!"


animals = [Dog("Buddy"), Cat("Whiskers")]
for animal in animals:
    print(f"{animal.name} says: {animal.make_sound()}")


# Multiple Inheritance
print("\n=== Multiple Inheritance ===")


class Employee:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class TimeKeeper:
    def __init__(self):
        self.current_time = 0

    def clock_in(self, time):
        self.current_time = time


class Manager(Employee, TimeKeeper):
    def __init__(self, id: int, name: str, department: str):
        Employee.__init__(self, id, name)
        TimeKeeper.__init__(self)
        self.department = department


manager = Manager(1, "John Doe", "IT")
manager.clock_in(9)
print(f"Manager {manager.name} clocked in at {manager.current_time}")


# Abstract Base Classes
print("\n=== Abstract Base Classes ===")


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


rect = Rectangle(5, 3)
print(f"Rectangle area: {rect.area()}")
print(f"Rectangle perimeter: {rect.perimeter()}")


# Duck Typing and Polymorphism
print("\n=== Duck Typing and Polymorphism ===")


class TextProcessor:
    def process(self, text: str) -> str:
        pass


class Uppercase(TextProcessor):
    def process(self, text: str) -> str:
        return text.upper()


class Lowercase(TextProcessor):
    def process(self, text: str) -> str:
        return text.lower()


def process_text(processor: TextProcessor, text: str) -> str:
    return processor.process(text)


text = "Hello World"
print(f"Uppercase: {process_text(Uppercase(), text)}")
print(f"Lowercase: {process_text(Lowercase(), text)}")


# Extending Built-in Types
print("\n=== Extending Built-in Types ===")


class CustomList(list):
    def map(self, func):
        return CustomList(map(func, self))

    def filter(self, func):
        return CustomList(filter(func, self))


numbers = CustomList([1, 2, 3, 4, 5])
evens = numbers.filter(lambda x: x % 2 == 0)
doubled = evens.map(lambda x: x * 2)
print(f"Original: {numbers}")
print(f"Evens: {evens}")
print(f"Doubled evens: {doubled}")


# Data Classes
print("\n=== Data Classes ===")


@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0

    @property
    def total_value(self) -> float:
        return self.price * self.quantity


product = Product("Phone", 999.99, 5)
print(f"Product: {product}")
print(f"Total value: ${product.total_value:.2f}")


# Real-world Example: E-commerce System
print("\n=== Real-world Example: E-commerce System ===")


class Discount(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass


class PercentageDiscount(Discount):
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply(self, amount: float) -> float:
        return amount * (1 - self.percentage / 100)


class FlatDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, amount: float) -> float:
        return max(0, amount - self.amount)


@dataclass
class OrderItem:
    product: Product
    quantity: int

    @property
    def total(self) -> float:
        return self.product.price * self.quantity


class Order:
    def __init__(self, items: List[OrderItem], discount: Discount = None):
        self.items = items
        self.discount = discount

    @property
    def subtotal(self) -> float:
        return sum(item.total for item in self.items)

    @property
    def total(self) -> float:
        if self.discount:
            return self.discount.apply(self.subtotal)
        return self.subtotal


# Create products
phone = Product("Phone", 999.99)
case = Product("Phone Case", 29.99)

# Create order with items
order = Order([OrderItem(phone, 1), OrderItem(case, 2)], PercentageDiscount(10))

print(f"Order subtotal: ${order.subtotal:.2f}")
print(f"Order total with 10% discount: ${order.total:.2f}")
