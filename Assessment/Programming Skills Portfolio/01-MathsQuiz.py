import random
import tkinter as tk

win = tk.Tk()
win.title("Maths Quiz")
win.geometry("400x280")

mode = ""


def wipe():
    # clear old widgets before drawing next screen
    for item in win.winfo_children():
        item.destroy()


def displayMenu():
    wipe()
    tk.Label(win, text="DIFFICULTY LEVEL", font=("Arial", 14, "bold")).pack(pady=15)
    tk.Button(win, text="1. Easy", width=15, command=lambda: pick("Easy")).pack(pady=4)
    tk.Button(win, text="2. Moderate", width=15, command=lambda: pick("Moderate")).pack(pady=4)
    tk.Button(win, text="3. Advanced", width=15, command=lambda: pick("Advanced")).pack(pady=4)


def randomInt(diff):
    # digit ranges from the brief
    if diff == "Easy":
        x = random.randint(1, 9)
        y = random.randint(1, 9)
    elif diff == "Moderate":
        x = random.randint(10, 99)
        y = random.randint(10, 99)
    else:
        x = random.randint(1000, 9999)
        y = random.randint(1000, 9999)
    return x, y


def decideOperation():
    op = random.choice(["+", "-"])
    return op


def pick(m):
    global mode
    mode = m
    n1, n2 = randomInt(mode)
    sign = decideOperation()
    print(n1, sign, n2)  # quick check in terminal while building


displayMenu()
win.mainloop()