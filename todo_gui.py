import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Specify the directory and filename
directory = "/home/example/"  # Replace with your desired directory
filename = "tasks_gui.json"
filepath = os.path.join(directory, filename)

# Load tasks function
def load_tasks(task_listbox):
    try:
        with open(filepath, "r") as file:
            json_tasks = json.load(file)
            for json_task in json_tasks:
                task = Task(**json_task)
                tasks.append(task)
                task_listbox.insert(tk.END, task.display())
    except FileNotFoundError:
        return

# Save tasks function
def save_tasks():
    with open(filepath, "w") as file:
        json_tasks = [task.__dict__ for task in tasks]
        json.dump(json_tasks, file, indent=4)

# Class to categorize tasks
class Task:
    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self.priority = priority

    def display(self):
        return f"Priority: {self.priority}, {self.title}"

# List of tasks
tasks = []

# Function to create the main window
def create_main_window():
    window = tk.Tk()
    window.title("Todo List")
    window.geometry("800x600")

    # Listbox to display tasks
    task_listbox = tk.Listbox(window, width=100, height=25)
    task_listbox.pack(pady=20)

    # Load tasks into the listbox on startup
    load_tasks(task_listbox)

    # Create a frame to hold the buttons
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    # Button to add a new task
    add_button = tk.Button(button_frame, text="Add Task", command=lambda: add_task(task_listbox))
    add_button.grid(row=0, column=0, padx=5, pady=5)

    # Button to delete a selected task
    delete_button = tk.Button(button_frame, text="Delete Task", command=lambda: delete_task(task_listbox))
    delete_button.grid(row=0, column=1, padx=5, pady=5)

    # Button to view/edit a selected task
    edit_button = tk.Button(button_frame, text="View/Edit Task", command=lambda: edit_task(task_listbox))
    edit_button.grid(row=0, column=2, padx=5, pady=5)

    # Button to save tasks
    save_button = tk.Button(button_frame, text="Save", command=save_tasks)
    save_button.grid(row=0, column=3, padx=5, pady=5)

    # Button to move task up
    move_up_button = tk.Button(button_frame, text="Move Task Up", command=lambda: move_task_up(task_listbox))
    move_up_button.grid(row=0, column=4, padx=5, pady=5)

    # Button to move task down
    move_down_button = tk.Button(button_frame, text="Move Task Down", command=lambda: move_task_down(task_listbox))
    move_down_button.grid(row=0, column=5, padx=5, pady=5)

    window.mainloop()

# Adding move task up functionality
def move_task_up(task_listbox):
    try:
        selected_index = task_listbox.curselection()[0]
        if selected_index > 0:  # Can't move the first task up
            # Swap the selected task with the one above it
            tasks[selected_index], tasks[selected_index - 1] = tasks[selected_index - 1], tasks[selected_index]
            
            # Update the Listbox display
            task_listbox.delete(0, tk.END)
            for task in tasks:
                task_listbox.insert(tk.END, task.display())
            
            # Update the selection in the Listbox
            task_listbox.select_set(selected_index - 1)
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to move up.")

# Adding move task down functionality
def move_task_down(task_listbox):
    try:
        selected_index = task_listbox.curselection()[0]
        if selected_index < len(tasks) - 1:  # Can't move the last task down
            # Swap the selected task with the one below it
            tasks[selected_index], tasks[selected_index + 1] = tasks[selected_index + 1], tasks[selected_index]
            
            # Update the Listbox display
            task_listbox.delete(0, tk.END)
            for task in tasks:
                task_listbox.insert(tk.END, task.display())
            
            # Update the selection in the Listbox
            task_listbox.select_set(selected_index + 1)
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to move down.")

# Function to add a task
def add_task(task_listbox):
    # Create a new window to enter task details
    task_window = tk.Toplevel()
    task_window.title("Add Task")

    tk.Label(task_window, text="Title:").grid(row=0, column=0, padx=10, pady=5)
    title_entry = tk.Entry(task_window)
    title_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(task_window, text="Description:").grid(row=1, column=0, padx=10, pady=5)
    description_entry = tk.Entry(task_window)
    description_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(task_window, text="Priority:").grid(row=2, column=0, padx=10, pady=5)
    priority_entry = tk.Entry(task_window)
    priority_entry.grid(row=2, column=1, padx=10, pady=5)

    def save_new_task():
        title = title_entry.get()
        description = description_entry.get()
        priority = priority_entry.get()
        if title and description and priority:
            task = Task(title, description, priority)
            tasks.append(task)
            task_listbox.insert(tk.END, task.display())
            task_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    save_button = tk.Button(task_window, text="Save Task", command=save_new_task)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

# Function to delete a task
def delete_task(task_listbox):
    try:
        selected_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_index)
        del tasks[selected_index]
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to delete.")

# Function to view/edit a task
def edit_task(task_listbox):
    try:
        selected_index = task_listbox.curselection()[0]
        selected_task = tasks[selected_index]

        # Create a new window for editing
        edit_window = tk.Toplevel()
        edit_window.title("Edit Task")

        # Title label and entry
        title_label = tk.Label(edit_window, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=10)
        title_entry = tk.Entry(edit_window, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=10)
        title_entry.insert(0, selected_task.title)  # Pre-fill with current title

        # Description label and entry
        description_label = tk.Label(edit_window, text="Description:")
        description_label.grid(row=1, column=0, padx=10, pady=10)
        description_entry = tk.Entry(edit_window, width=40)
        description_entry.grid(row=1, column=1, padx=10, pady=10)
        description_entry.insert(0, selected_task.description)  # Pre-fill with current description

        # Priority label and entry
        priority_label = tk.Label(edit_window, text="Priority:")
        priority_label.grid(row=2, column=0, padx=10, pady=10)
        priority_entry = tk.Entry(edit_window, width=40)
        priority_entry.grid(row=2, column=1, padx=10, pady=10)
        priority_entry.insert(0, selected_task.priority)  # Pre-fill with current priority

        # Save button
        save_button = tk.Button(edit_window, text="Save Changes", command=lambda: save_edited_task(selected_index, title_entry.get(), description_entry.get(), priority_entry.get(), task_listbox, edit_window))
        save_button.grid(row=3, columnspan=2, pady=20)

    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to view/edit.")

# Function to save the edited task
def save_edited_task(index, new_title, new_description, new_priority, task_listbox, edit_window):
    # Update the task details
    tasks[index].title = new_title
    tasks[index].description = new_description
    tasks[index].priority = new_priority

    # Update the Listbox display
    task_listbox.delete(index)
    task_listbox.insert(index, tasks[index].display())

    # Close the edit window
    edit_window.destroy()

# Load file & Create the main window
create_main_window()
