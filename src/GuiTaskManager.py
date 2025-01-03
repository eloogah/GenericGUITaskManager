import tkinter as tk
from datetime import datetime
import json
import os
from tkinter import ttk  # For better looking widgets

def get_current_time():
    return datetime.now().strftime("%I:%M %p")

root = tk.Tk()
root.title("Generic Gui Task Manager")
root.geometry("800x600")
root.configure(bg='#2C3E50')

# Create listbox to display tasks
task_list = tk.Listbox(root, height=20, width=70)
task_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


TASKS_FILE = "tasks.json"

# Function to load tasks
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
            for task in tasks:
                task_list.insert(tk.END, task)

# Function to save tasks
def save_tasks():
    tasks = task_list.get(0, tk.END)
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

# Load tasks when the application starts
load_tasks()

# Create the root window

# Create task input area
input_frame = ttk.Frame(root, padding="10")
input_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

task_label = ttk.Label(input_frame, text="Task:")
task_label.grid(row=0, column=0, padx=5, pady=5)

task_entry = ttk.Entry(input_frame, width=30)
task_entry.grid(row=0, column=1, padx=5, pady=5)

time_label = ttk.Label(input_frame, text="Time:")
time_label.grid(row=0, column=2, padx=5, pady=5)

time_entry = ttk.Entry(input_frame, width=10)
time_entry.grid(row=0, column=3, padx=5, pady=5)

"""
# Create "Time Until" column
time_until_label = ttk.Label(input_frame, text="Time Until:")
time_until_label.grid(row=0, column=6, padx=5, pady=5)

time_until_var = tk.StringVar()
time_until_entry = ttk.Entry(input_frame, textvariable=time_until_var, width=10, state='readonly')
time_until_entry.grid(row=0, column=7, padx=5, pady=5)
"""

# Create dropdown menu for AM/PM
ampm_label = ttk.Label(input_frame, text="AM/PM:")
ampm_label.grid(row=0, column=4, padx=5, pady=5)

ampm_var = tk.StringVar()
ampm_dropdown = ttk.Combobox(input_frame, textvariable=ampm_var, values=["AM", "PM", " "], width=5)
ampm_dropdown.grid(row=0, column=5, padx=5, pady=5)
ampm_dropdown.current(0)

"""
def update_time_until(*args):
    try:
        task_time_str = time_entry.get() + " " + ampm_var.get()
        task_time = datetime.strptime(task_time_str, "%I:%M %p")
        current_time = datetime.now().replace(second=0, microsecond=0)
        if task_time < current_time:
            task_time = task_time.replace(day=current_time.day + 1)
        time_until = task_time - current_time
        time_until_var.set(str(time_until))
    except ValueError:
        time_until_var.set("Invalid time")


time_entry.bind("<KeyRelease>", update_time_until)
ampm_var.trace("w", update_time_until)
"""

# Function to add tasks
def add_task():
    task = task_entry.get()
    time = time_entry.get()
    ampm = ampm_var.get()
    if task and time:
        task_list.insert(tk.END, f"{task} - {time} {ampm}")
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)

# Function to delete selected task
def delete_task():
    try:
        selected = task_list.curselection()
        task_list.delete(selected)
    except:
        pass

def priority_down():
    try:
        selected = task_list.curselection()
        task = task_list.get(selected)
        task_list.delete(selected)
        task_list.insert(selected[0] + 1, task)
    except:
        pass

def priority_up():
    try:
        selected = task_list.curselection()
        task = task_list.get(selected)
        task_list.delete(selected)
        task_list.insert(selected[0] - 1, task)
    except:
        pass

# Save tasks when the application closes
root.protocol("WM_DELETE_WINDOW", lambda: [save_tasks(), root.destroy()])

# Add buttons
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

add_button = ttk.Button(button_frame, text="Add Task", command=add_task)
add_button.grid(row=0, column=0, padx=5, pady=5)

delete_button = ttk.Button(button_frame, text="Delete Task", command=delete_task)
delete_button.grid(row=0, column=1, padx=5, pady=5)

priority_up_button = ttk.Button(button_frame, text="Priority Up", command=priority_up)
priority_up_button.grid(row=0, column=2, padx=5, pady=5)

priority_down_button = ttk.Button(button_frame, text="Priority Down", command=priority_down)
priority_down_button.grid(row=0, column=3, padx=5, pady=5)

# Allow the columns and rows to expand with window resizing
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

root.mainloop()