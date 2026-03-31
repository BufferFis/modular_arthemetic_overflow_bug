#!/bin/bash
echo "Compiling C and Java files..."
gcc -std=c99 -Wall -Wextra -o nuclear_gandhi nuclear_gandhi.c
javac java-int-overflow.java

echo "Starting Tkinter UI..."
python3 main_ui.py
