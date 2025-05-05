#!/bin/bash
# Run a specific ExerciseN.py script in the Exercise directory based on user input

read -p "Enter exercise number to run (1-6): " ex_num

script="Exercise${ex_num}.py"

if [ -f "$script" ]; then
    echo "==============================="
    echo "Running $script"
    echo "==============================="
    python3 "$script"
    echo "\n"
else
    echo "No script found for exercise $ex_num."
fi
