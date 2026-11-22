import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# putting the txt file path next to the script so it doesnt break on another pc
base_dir = os.path.dirname(__file__)
marks_file = os.path.join(base_dir, "studentMarks.txt")

students = []  # each item: [code, name, cw_total, exam]

f = open(marks_file, "r")
lines = f.readlines()[1:]  # skipping line 1 since it just has the student count
f.close()

for line in lines:
    line = line.strip()
    if line:
        parts = line.split(",")
        cw_sum = int(parts[2]) + int(parts[3]) + int(parts[4])  # 3 coursework marks out of 20 each
        students.append([int(parts[0]), parts[1], cw_sum, int(parts[5])])


def get_pct(s):
    
    return ((s[2] + s[3]) / 160) * 100


def get_grade(p):
    if p >= 70:
        return "A"
    elif p >= 60:
        return "B"
    elif p >= 50:
        return "C"
    elif p >= 40:
        return "D"
    else:
        return "F"


def make_row(s):
    p = get_pct(s)
    g = get_grade(p)
    return f"{s[1]} ({s[0]}) | CW: {s[2]}/60 | Exam: {s[3]}/100 | {p:.1f}% | Grade: {g}"


def show_output(text):
    # cleared box first so old stuff stays gone
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)


def view_all():
    if not students:
        show_output("No student records found.")
        return

    msg = ""
    total_pct = 0
    for s in students:
        msg += make_row(s) + "\n"
        total_pct += get_pct(s)

    avg = total_pct / len(students)
    msg += f"\nTotal Students: {len(students)} | Average: {avg:.1f}%"
    show_output(msg)


def view_one():
    query = simpledialog.askstring("Find Student", "Enter name or student code:")
    if not query:
        return

    q = query.strip().lower()
    for s in students:
        if str(s[0]) == q or s[1].lower() == q:
            show_output(make_row(s))
            return

    messagebox.showinfo("Not Found", "Couldn't find that student.")


# basic gui setup
root = tk.Tk()
root.title("Student Manager")
root.geometry("760x400")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=8)

tk.Button(btn_frame, text="View All", width=16, command=view_all).pack(side=tk.LEFT, padx=4)
tk.Button(btn_frame, text="View Individual", width=16, command=view_one).pack(side=tk.LEFT, padx=4)

output_box = tk.Text(root, height=17, width=90, font=("Consolas", 10))
output_box.pack(padx=10, pady=4)

root.mainloop()