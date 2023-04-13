import tkinter as tk
import sqlite3

# Connect to the database
conn = sqlite3.connect('kalkulaator.db')
c = conn.cursor()

# Create the table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS calculations
             (num1 REAL, num2 REAL, operation TEXT, result REAL)''')

# Define the calculator functions
def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

# Define the calculate function
def calculate():
    num1 = float(num1_entry.get())
    num2 = float(num2_entry.get())
    operation = operation_var.get()
    if operation == "+":
        result = add(num1, num2)
    elif operation == "-":
        result = subtract(num1, num2)
    elif operation == "*":
        result = multiply(num1, num2)
    elif operation == "/":
        result = divide(num1, num2)
    result_label.config(text=result)
    num1_entry.delete(0, tk.END)
    num2_entry.delete(0, tk.END)
    # Store the calculation in the database
    c.execute("INSERT INTO calculations VALUES (?, ?, ?, ?)", (num1, num2, operation, result))
    conn.commit()
    # Add the calculation to the history list
    calc_history.append(f"{num1} {operation} {num2} = {result}")
    # Clear the history text widget
    history_text.delete('1.0', tk.END)
    # Update the history text widget with the new history list
    for history_item in calc_history:
        history_text.insert(tk.END, history_item + "\n")

# Define the function to toggle the history
def update_history():
    global show_history_button
    if show_history_button["text"] == "Show History":
        show_history_button["text"] = "Hide History"
        for history_item in calc_history:
            history_text.insert(tk.END, history_item + "\n")
    else:
        show_history_button["text"] = "Show History"
        history_text.delete('1.0', tk.END)

# Create the main window
root = tk.Tk()
root.title("Calculator")

# Create the number entry fields
num1_entry = tk.Entry(root)
num1_entry.grid(row=0, column=0)

num2_entry = tk.Entry(root)
num2_entry.grid(row=0, column=2)

# Create the operation dropdown menu
operation_var = tk.StringVar(root)
operation_var.set("+") # default value

operation_dropdown = tk.OptionMenu(root, operation_var, "+", "-", "*", "/")
operation_dropdown.grid(row=0, column=1)

# Create the calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate)
calculate_button.grid(row=1, column=2)

# Create the result label
result_label = tk.Label(root, text="")
result_label.grid(row=1, column=0)

# Create the history text widget
history_text = tk.Text(root, height=5, width=30)
history_text.grid(row=2, column=0, columnspan=3)

# Create the toggle
show_history_button = tk.Button(root, text="Show History", command=update_history)
show_history_button.grid(row=3, column=0, columnspan=3)

calc_history = []
for row in c.execute("SELECT * FROM calculations"):
    num1, num2, operation, result = row
    calc_history.append(f"{num1} {operation} {num2} = {result}")

conn.close()
root.mainloop()