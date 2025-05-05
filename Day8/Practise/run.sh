#!/bin/bash
# Run a specific Python script in the Ex directory based on user input

EX_DIR="$(dirname "$0")/Ex"

read -p "Enter exercise number to run (1-10): " ex_num

# Format exercise number to match file pattern (e.g., 1 -> ex1_, 10 -> ex10_)
pattern="ex${ex_num}_*.py"

found=0
for file in "$EX_DIR"/$pattern; do
    if [ -f "$file" ]; then
        found=1
        echo "==============================="
        echo "Running $file"
        echo "==============================="
        python3 "$file"
        echo "\n"
    fi
done

if [ $found -eq 0 ]; then
    echo "No script found for exercise $ex_num."
fi
