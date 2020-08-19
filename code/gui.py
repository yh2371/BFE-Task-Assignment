import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import threading
from bfehelper import *
from bfeclasses import *
from onoff import *
from shortestpath import *

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")

def gather_task():
    global checkerlist
    global daycounts
    txt_edit.delete('1.0', tk.END)
    data = data_file.get()
    checker = checker_file.get()
    num = int(sample_num.get())
    m = month.get()
    y = year.get()
    window = float(shift_window.get())
    incre = float(shift_incre.get())
    min_num = int(min_task.get())
    max_num = int(max_task.get())
    checkerlist = construct_checkerlist(checker)
    daycounts = get_ratio(checkerlist, num)
    select_cleaned_data(data, daycounts)
    x = threading.Thread(target=get_allchecker_tasks, args = (checkerlist, "sample450.csv", "LIC", "LIC", min_num, max_num, ["B", "S", "M", "Q", "BX"], incre, window, txt_edit))
    x.start()

def gen_schedule():
    global schedule
    txt_edit.delete('1.0', tk.END)
    checkerlist.get_uniqueness_score("sample450.csv")
    checkerlist.restructure()
    schedule = generate_schedule(checkerlist, "sample450.csv", 1, txt_edit)
    y = threading.Thread(target = evaluate_empty_days, args = (checkerlist, "sample450.csv", schedule, daycounts, txt_edit))
    y.start()

def refresh_schedule():
    txt_edit.delete('1.0', tk.END)
    txt_edit.insert(tk.END, "\nPrevious Schedule Results:\n")
    schedule.evaluate(txt_edit)
    refresh_week = int(refresh_point.get())-1
    missed = get_random_missing(schedule, 10)
    txt_edit.insert(tk.END, "\nMissed:\n")
    for i in missed:
        txt_edit.insert(tk.END, str(i)+", ")
    schedule.refresh(missed, refresh_week)
    txt_edit.insert(tk.END, "\n\nRefreshed Schedule Results:\n")
    #schedule.evaluate(txt_edit)
    schedule.evaluate_refresh(missed, refresh_week, txt_edit)

def save_file():
    """Save the current file as a new file."""
    #filepath = asksaveasfilename(
    #    defaultextension="csv",
    #    filetypes=[("Text Files", "*.csv"), ("All Files", "*.*")],
    #)
    #if not filepath:
    #    return
    m = month.get()
    y = year.get()
    schedule.export("sample.xls")
    txt_edit.insert(tk.END, "\nSchedule exported successfully")

def clear():
    """Clear all fields"""
    data_file.delete(0, tk.END)
    checker_file.delete(0, tk.END)
    sample_num.delete(0, tk.END)
    month.delete(0, tk.END)
    year.delete(0, tk.END)
    min_task.delete(0, tk.END)
    max_task.delete(0, tk.END)
    shift_window.delete(0, tk.END)
    shift_incre.delete(0, tk.END)
    txt_edit.delete('1.0', tk.END)
    refresh_point.delete(0, tk.END)
    missing_file.delete(0, tk.END)

window = tk.Tk()
window.title("Bus Fare Task Assignment System")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=550, weight=1)
window.columnconfigure(0, minsize=550, weight=1)

txt_edit = tk.Text(window, undo = False)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_gather = tk.Button(fr_buttons, text="Gather Tasks", command=gather_task)
btn_gen = tk.Button(fr_buttons, text="Generate Schedule", command=gen_schedule)
btn_exp = tk.Button(fr_buttons, text="Export Schedule", command=save_file)
btn_ref = tk.Button(fr_buttons, text="Refresh Schedule", command=refresh_schedule)
btn_clear = tk.Button(fr_buttons, text="Clear", command=clear)

data_file = tk.Entry(fr_buttons)
datafile_label = tk.Label(fr_buttons, text="Sample Data File")
checker_file = tk.Entry(fr_buttons)
checkerfile_label = tk.Label(fr_buttons, text="Checker Data File")
sample_num = tk.Entry(fr_buttons)
num_label = tk.Label(fr_buttons, text ="Number of Random Samples")
month = tk.Entry(fr_buttons)
month_label = tk.Label(fr_buttons, text="Month")
year = tk.Entry(fr_buttons)
year_label = tk.Label(fr_buttons, text="Year")
min_task = tk.Entry(fr_buttons)
min_label = tk.Label(fr_buttons, text="Minimum Samples Per Day")
max_task = tk.Entry(fr_buttons)
max_label = tk.Label(fr_buttons, text="Maximum Samples Per Day")
shift_window = tk.Entry(fr_buttons)
shift_window_label= tk.Label(fr_buttons, text="Shift Window (hours)")
shift_incre = tk.Entry(fr_buttons)
shift_incre_label = tk.Label(fr_buttons, text="Shift Increments (hours)")
refresh_point= tk.Entry(fr_buttons)
refresh_point_label = tk.Label(fr_buttons, text="Refresh Week Number")
missing_file= tk.Entry(fr_buttons)
missing_file_label = tk.Label(fr_buttons, text="Missing Data File")
previous_file= tk.Entry(fr_buttons)
previous_file_label = tk.Label(fr_buttons, text="Schedule to be Updated")

blank_label = tk.Label(fr_buttons, text="\t")
blank_label2 = tk.Label(fr_buttons, text="\t")
blank_label3 = tk.Label(fr_buttons, text="\t")
blank_label4 = tk.Label(fr_buttons, text="\t")
data_file.grid(row = 1, column = 2, sticky ="nsew")
datafile_label.grid(row = 1, column = 1,sticky ="w")
checkerfile_label.grid(row =2, column = 1, sticky = "w")
checker_file.grid(row = 2, column = 2, sticky ="nsew")
blank_label.grid(row=0, column = 0)
blank_label2.grid(row=1, column = 0)
blank_label4.grid(row=2, column = 0)
blank_label3.grid(row=13, column = 0)

sample_num.grid(row = 5, column = 2, sticky = "nsew")
num_label.grid(row=5, column = 1, sticky ="w")
month_label.grid(row=6, column = 1, sticky ="w")
month.grid(row=6, column=2, sticky="nsew")
year_label.grid(row=7,column=1, sticky="w")
year.grid(row=7, column=2, sticky="nsew")
min_label.grid(row=8, column = 1, sticky ="w")
min_task.grid(row=8, column=2, sticky="nsew")
max_label.grid(row=9, column = 1, sticky ="w")
max_task.grid(row=9, column=2, sticky="nsew")
shift_window_label.grid(row=10, column = 1, sticky ="w")
shift_window.grid(row=10, column=2, sticky="nsew")
shift_incre_label.grid(row=11, column = 1, sticky ="w")
shift_incre.grid(row=11, column=2, sticky="nsew")
refresh_point_label.grid(row=12, column = 1, sticky ="w")
refresh_point.grid(row=12, column=2, sticky="nsew")
missing_file_label.grid(row=3, column = 1, sticky ="w")
missing_file.grid(row=3, column=2, sticky="nsew")
previous_file_label.grid(row=4, column = 1, sticky ="w")
previous_file.grid(row=4, column=2, sticky="nsew")

btn_gather.grid(row=14, column=1, sticky="ew", padx=5, pady=5)
btn_gen.grid(row=15, column=1, sticky="ew", padx=5, pady=5)
btn_exp.grid(row=16, column=1, sticky="ew", padx=5, pady=5)
btn_ref.grid(row=17, column=1, sticky="ew", padx=5, pady=5)
btn_clear.grid(row=18, column=1, sticky="ew", padx=5, pady=5)

fr_buttons.grid(row=0, column=0, sticky="nsew")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
