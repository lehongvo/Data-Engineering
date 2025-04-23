from pathlib import Path
import shutil
import zipfile
import csv
import json
import sqlite3
from datetime import datetime, timedelta
import time
import random
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import subprocess
from string import Template
import os

# Working with Paths
print("\n=== Working with Paths ===")
path = Path("data/test.txt")
print(f"Path: {path}")
print(f"Parent: {path.parent}")
print(f"Name: {path.name}")
print(f"Stem: {path.stem}")
print(f"Suffix: {path.suffix}")
print(f"Exists: {path.exists()}")

# Working with Directories
print("\n=== Working with Directories ===")
data_dir = Path("data")
if not data_dir.exists():
    data_dir.mkdir()
    print(f"Created directory: {data_dir}")

# List all python files in current directory
python_files = [f for f in Path().glob("*.py")]
print("Python files:", python_files)

# Working with Files
print("\n=== Working with Files ===")
file_path = data_dir / "sample.txt"
# Writing to file
file_path.write_text("Hello, World!\nThis is a test file1.")
print(f"Written to {file_path}")

# Reading from file
content = file_path.read_text()
print(f"File content:\n{content}")

# Working with ZIP Files
print("\n=== Working with ZIP Files ===")
with zipfile.ZipFile("data/archive.zip", "w") as zf:
    zf.write(file_path)
print("Created ZIP file with sample.txt")

# Working with CSV Files
print("\n=== Working with CSV Files ===")
csv_path = data_dir / "data.csv"
# Writing CSV
with open(csv_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Age", "City"])
    writer.writerow(["John", 30, "New York"])
    writer.writerow(["Alice", 25, "London"])

# Reading CSV
with open(csv_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Working with JSON Files
print("\n=== Working with JSON Files ===")
person = {
    "name": "John Doe",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "music"],
}

json_path = data_dir / "data.json"
# Writing JSON
with open(json_path, "w") as file:
    json.dump(person, file, indent=4)

# Reading JSON
with open(json_path, "r") as file:
    loaded_data = json.load(file)
print(f"Loaded JSON: {loaded_data}")

# Working with SQLite Database
print("\n=== Working with SQLite Database ===")
db_path = data_dir / "database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
"""
)

# Insert data
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("John", 30))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
conn.commit()

# Query data
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("Database users:", users)
conn.close()

# Working with Timestamps and DateTimes
print("\n=== Working with Timestamps and DateTimes ===")
now = datetime.now()
print(f"Current datetime: {now}")
print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Working with Time Deltas
print("\n=== Working with Time Deltas ===")
future = now + timedelta(days=7)
print(f"7 days from now: {future}")
difference = future - now
print(f"Time difference: {difference}")

# Generating Random Values
print("\n=== Generating Random Values ===")
print(f"Random integer (1-10): {random.randint(1, 10)}")
print(f"Random choice from list: {random.choice(['apple', 'banana', 'orange'])}")
print(f"Random float (0-1): {random.random()}")

# Opening the Browser
print("\n=== Opening the Browser ===")
# Commented out to prevent browser opening
# webbrowser.open("http://google.com")

# Sending Emails (Example setup - credentials needed)
print("\n=== Email Setup Example ===")


def send_email_example():
    sender = "your_email@gmail.com"
    receiver = "recipient@example.com"
    password = "your_password"

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Test Email"

    body = "This is a test email sent from Python!"
    message.attach(MIMEText(body, "plain"))

    print("Email setup complete (not sent - needs credentials)")


send_email_example()

# Templates
print("\n=== Working with Templates ===")
template_text = Template("Hello, $name! Your balance is $$balance.")
message = template_text.substitute(name="John", balance="1000")
print(message)

# Command-line Arguments
print("\n=== Command-line Arguments ===")
print(f"Script name: {sys.argv[0]}")
print(f"All arguments: {sys.argv}")

# Running External Programs
print("\n=== Running External Programs ===")
try:
    # List directory contents
    result = subprocess.run(["ls", "-l"], capture_output=True, text=True)
    print("Directory listing:")
    print(result.stdout)
except FileNotFoundError:
    print("Command not found")

# Cleanup
print("\n=== Cleanup ===")
# Uncomment to cleanup test files
# shutil.rmtree(data_dir)
print("Test files kept for inspection")
