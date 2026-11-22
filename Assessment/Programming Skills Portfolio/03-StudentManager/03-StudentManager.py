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


def save_data():
    # write count first so the file format stays the same as the original
    f = open(marks_file, "w")
    f.write(str(len(students)) + "\n")
    for s in students:
        # split cw total back into 3 pieces roughly so the txt file stays valid
        each = s[2] // 3
        rem = s[2] % 3
        f.write(f"{s[0]},{s[1]},{each},{each},{each + rem},{s[3]}\n")
    f.close()


def get_pct(s):
    # coursework is 60 + exam is 100 = 160 total
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
    # clear box first so old stuff stays gone
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, text)


def find_student(query):
    q = query.strip().lower()
    for s in students:
        if str(s[0]) == q or s[1].lower() == q:
            return s
    return None


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

    s = find_student(query)
    if s:
        show_output(make_row(s))
    else:
        messagebox.showinfo("Not Found", "Couldn't find that student.")


def show_highest():
    if not students:
        show_output("No student records found.")
        return

    # start with first student and swap if someone has a higher pct
    top = students[0]
    for s in students:
        if get_pct(s) > get_pct(top):
            top = s

    show_output("Highest Score:\n" + make_row(top))


def show_lowest():
    if not students:
        show_output("No student records found.")
        return

    # same idea as highest, just looking for smaller pct
    low = students[0]
    for s in students:
        if get_pct(s) < get_pct(low):
            low = s

    show_output("Lowest Score:\n" + make_row(low))


def sort_students():
    if not students:
        show_output("No student records found.")
        return

    order = simpledialog.askstring("Sort Records", "Type 'asc' or 'desc':")
    if not order:
        return

    order = order.strip().lower()
    if order == "asc":
        ordered = sorted(students, key=get_pct)
    elif order == "desc":
        ordered = sorted(students, key=get_pct, reverse=True)
    else:
        messagebox.showwarning("Invalid Choice", "Please type asc or desc.")
        return

    msg = f"Sorted ({order}):\n"
    for s in ordered:
        msg += make_row(s) + "\n"
    show_output(msg)


def add_student():
    try:
        code = int(simpledialog.askstring("Add Student", "Student code (1000-9999):"))
        name = simpledialog.askstring("Add Student", "Student name:").strip()
        c1 = int(simpledialog.askstring("Add Student", "Coursework 1 (0-20):"))
        c2 = int(simpledialog.askstring("Add Student", "Coursework 2 (0-20):"))
        c3 = int(simpledialog.askstring("Add Student", "Coursework 3 (0-20):"))
        exam = int(simpledialog.askstring("Add Student", "Exam mark (0-100):"))
    except Exception:
        messagebox.showwarning("Input Error", "Check your numbers and try again.")
        return

    if not name or code < 1000 or code > 9999:
        messagebox.showwarning("Input Error", "Need a valid name and 4-digit code.")
        return

    students.append([code, name, c1 + c2 + c3, exam])
    save_data()
    view_all()


def delete_student():
    query = simpledialog.askstring("Delete Student", "Enter name or student code:")
    if not query:
        return

    s = find_student(query)
    if not s:
        messagebox.showinfo("Not Found", "Couldn't find that student.")
        return

    # remove from list and update the txt file
    students.remove(s)
    save_data()
    view_all()


def update_student():
    query = simpledialog.askstring("Update Student", "Enter name or student code:")
    if not query:
        return

    s = find_student(query)
    if not s:
        messagebox.showinfo("Not Found", "Couldn't find that student.")
        return

    choice = simpledialog.askstring("Update Field", "Update what? (name, cw, exam)")
    if not choice:
        return

    choice = choice.strip().lower()
    try:
        if choice == "name":
            new_name = simpledialog.askstring("Update Name", "New name:")
            if new_name and new_name.strip():
                s[1] = new_name.strip()
        elif choice == "cw":
            c1 = int(simpledialog.askstring("Coursework", "CW 1 (0-20):"))
            c2 = int(simpledialog.askstring("Coursework", "CW 2 (0-20):"))
            c3 = int(simpledialog.askstring("Coursework", "CW 3 (0-20):"))
            s[2] = c1 + c2 + c3
        elif choice == "exam":
            s[3] = int(simpledialog.askstring("Exam", "New exam mark (0-100):"))
        else:
            messagebox.showwarning("Invalid Choice", "Type name, cw, or exam.")
            return
    except Exception:
        messagebox.showwarning("Input Error", "Enter a valid number.")
        return

    save_data()
    view_all()


# basic gui setup
root = tk.Tk()
root.title("Student Manager")
root.geometry("800x430")

row1 = tk.Frame(root)
row1.pack(pady=5)

tk.Button(row1, text="View All", width=15, command=view_all).pack(side=tk.LEFT, padx=3)
tk.Button(row1, text="View Individual", width=15, command=view_one).pack(side=tk.LEFT, padx=3)
tk.Button(row1, text="Highest Score", width=15, command=show_highest).pack(side=tk.LEFT, padx=3)
tk.Button(row1, text="Lowest Score", width=15, command=show_lowest).pack(side=tk.LEFT, padx=3)

row2 = tk.Frame(root)
row2.pack(pady=3)

tk.Button(row2, text="Sort Records", width=15, command=sort_students).pack(side=tk.LEFT, padx=3)
tk.Button(row2, text="Add Student", width=15, command=add_student).pack(side=tk.LEFT, padx=3)
tk.Button(row2, text="Delete Student", width=15, command=delete_student).pack(side=tk.LEFT, padx=3)
tk.Button(row2, text="Update Student", width=15, command=update_student).pack(side=tk.LEFT, padx=3)

output_box = tk.Text(root, height=18, width=94, font=("Consolas", 10))
output_box.pack(padx=10, pady=6)

root.mainloop()