import tkinter as tk
import random
import os

# get path to randomJokes.txt in this same folder
here = os.path.dirname(__file__)
joke_file = open(os.path.join(here, "randomJokes.txt"), "r")
raw_lines = joke_file.readlines()
joke_file.close()

# split each line into setup and punchline
jokes = []
for row in raw_lines:
    row = row.strip()
    if "?" in row:
        part = row.split("?")
        jokes.append([part[0] + "?", part[1]])