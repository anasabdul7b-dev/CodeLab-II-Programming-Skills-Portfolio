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

win = tk.Tk()
win.title("Alexa Joke Teller")
win.geometry("450x300")

punch = "" # keeps the punchline for the current joke

q_lbl = tk.Label(win, text="", font=("Arial", 12, "bold"), wraplength=380)
q_lbl.pack(pady=20)

a_lbl = tk.Label(win, text="", font=("Arial", 11), fg="darkblue", wraplength=380)
a_lbl.pack(pady=10)

def new_joke():
    global punch
    j = random.choice(jokes)
    q_lbl.config(text=j[0])
    punch = j[1]
    a_lbl.config(text="") # hide old punchline

def show_ans():
    if punch != "":
        a_lbl.config(text=punch)

# buttons
tk.Button(win, text="Alexa tell me a Joke", width=18, command=new_joke).pack(pady=4)
tk.Button(win, text="Show Punchline", width=18, command=show_ans).pack(pady=4)
tk.Button(win, text="Next Joke", width=18, command=new_joke).pack(pady=4)
tk.Button(win, text="Quit", width=18, command=win.destroy).pack(pady=10)

win.mainloop()