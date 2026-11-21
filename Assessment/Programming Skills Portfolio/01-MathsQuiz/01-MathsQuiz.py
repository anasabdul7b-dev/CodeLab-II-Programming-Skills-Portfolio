import random
import tkinter as tk
from tkinter import messagebox

win = tk.Tk()
win.title("Maths Quiz")
win.geometry("400x280")

# tracking quiz stuff
mode = ""
q = 0
score = 0
try_num = 1
n1 = 0
n2 = 0
sign = "+"
right_ans = 0
inp = None
err_lbl = None


def wipe():
    # clear old widgets before drawing next screen
    for item in win.winfo_children():
        item.destroy()


def displayMenu():
    wipe()
    tk.Label(win, text="DIFFICULTY LEVEL", font=("Arial", 14, "bold")).pack(pady=15)
    tk.Button(win, text="1. Easy", width=15, command=lambda: begin("Easy")).pack(pady=4)
    tk.Button(win, text="2. Moderate", width=15, command=lambda: begin("Moderate")).pack(pady=4)
    tk.Button(win, text="3. Advanced", width=15, command=lambda: begin("Advanced")).pack(pady=4)


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


def begin(m):
    global mode, q, score
    mode = m
    q = 0
    score = 0
    make_q()


def make_q():
    global q, try_num, n1, n2, sign, right_ans
    if q == 10:
        displayResults()
        return

    q += 1
    try_num = 1  # reset attempts for new question
    n1, n2 = randomInt(mode)
    sign = decideOperation()

    if sign == "+":
        right_ans = n1 + n2
    else:
        right_ans = n1 - n2

    displayProblem()


def displayProblem():
    global inp, err_lbl
    wipe()

    tk.Label(win, text=f"Question {q}/10 | Score: {score}").pack(pady=8)
    tk.Label(win, text=f"{n1} {sign} {n2} =", font=("Arial", 18, "bold")).pack(pady=10)

    inp = tk.Entry(win, width=10, justify="center")
    inp.pack(pady=5)
    inp.focus()
    inp.bind("<Return>", lambda e: send_ans())  # so enter key works too

    tk.Button(win, text="Submit", width=12, command=send_ans).pack(pady=8)

    err_lbl = tk.Label(win, text="")
    err_lbl.pack()


def isCorrect(guess):
    global score, try_num

    if guess == right_ans:
        if try_num == 1:
            score += 10
            messagebox.showinfo("Nice", "+10 points")
        else:
            score += 5
            messagebox.showinfo("Nice", "+5 points")
        return True

    # give one retry if they miss the first time
    if try_num == 1:
        try_num = 2
        err_lbl.config(text="Try again!", fg="orange")
        inp.delete(0, tk.END)
        inp.focus()
        return False

    messagebox.showinfo("Wrong", f"Answer was {right_ans}")
    return True


def send_ans():
    val = inp.get().strip()
    try:
        num = int(val)
    except ValueError:
        # stop crash if empty or not a number
        err_lbl.config(text="Enter a valid number", fg="red")
        return

    done = isCorrect(num)
    if done:
        make_q()


def displayResults():
    wipe()

    if score > 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "D"

    tk.Label(win, text="Finished!", font=("Arial", 15, "bold")).pack(pady=12)
    tk.Label(win, text=f"Score: {score}/100", font=("Arial", 12)).pack(pady=4)
    tk.Label(win, text=f"Rank: {grade}", font=("Arial", 12)).pack(pady=4)

    tk.Button(win, text="Play Again", width=14, command=displayMenu).pack(pady=10)
    tk.Button(win, text="Quit", width=14, command=win.destroy).pack()


displayMenu()
win.mainloop()