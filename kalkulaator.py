import tkinter as tk
from tkinter import messagebox
import sqlite3

class Calculator:
    def __init__(self, master):
        
          
        master.title("Calculator")
        self.master = master
        self.count = 0

        self.num1_entry = tk.Entry(master, width=10)
        self.num1_entry.grid(row=0, column=0)

        self.num2_entry = tk.Entry(master, width=10)
        self.num2_entry.grid(row=0, column=2)

        # Initialize the operation_var attribute
        self.operation_var = tk.StringVar(master)
        self.operation_var.set("+")  # default value

        # Create the operation dropdown menu
        self.operation_dropdown = tk.OptionMenu(master, self.operation_var, "+", "-", "*", "/")
        self.operation_dropdown.grid(row=0, column=1)

        # Create the calculate button
        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=1, column=2)

        # Create the result label
        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=1, column=0)

        # Create the history text widget and the show/hide history button
        self.history_text = tk.Text(master, height=10, width=20)
        self.history_text.grid(row=2, column=0, columnspan=3)

        self.show_history_button = tk.Button(master, text="Show History", command=self.toggle_history)
        self.show_history_button.grid(row=3, column=0, columnspan=2)

        self.delete_history_button = tk.Button(master, text="Delete History", command=self.delete_history)
        self.delete_history_button.grid(row=3, column=2)
        self.count_label = tk.Label(master, text="Count: 0")
        self.count_label.grid(row=4, column=0)
        self.count_label.config(text=f"Count: {self.count}")


        master.geometry("400x400")
        
        

        # Connect to the database and create the table if it does not exist
        self.conn = sqlite3.connect('calc_history.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS calculations
            (num1 REAL, num2 REAL, operation TEXT, result REAL)''')

    def calculate(self):
        

        # Retrieve the input values and operation
        num1 = float(self.num1_entry.get())
        num2 = float(self.num2_entry.get())
        operation = self.operation_var.get()

        # Perform the calculation and update the result label
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            result = num1 / num2
            
        self.count += 1  # increment the count
        self.update_count_display(num1, num2, operation, result)  # update the count display

        # Update the result label and the history
        self.result_label.config(text=str(result))
        history_str = f"{num1} {operation} {num2} = {result}\n"
        self.history_text.insert(tk.END, history_str)

    def update_count_display(self, num1, num2, operation, result):
        count_str = f"Total Calculations: {self.count}"
        self.count_label.config(text=count_str)

        # Save the calculation to the database
        self.c.execute("INSERT INTO calculations VALUES (?, ?, ?, ?)", (num1, num2, operation, result))
        self.conn.commit()
        
        
    def show_help(self):
        messagebox.showinfo("Help", "Sisestage numbrisisestusväljadele kaks numbrit, valige rippmenüüst toiming ja klõpsake arvutuse tegemiseks nuppu 'Calculate'. Tulemus kuvatakse sildil. Klõpsake nuppu 'Show History', et vaadata varasemaid arvutusi. 'Delete History' kustutab ajaloost kõik varasemad tehted ära.  PÄRAST SEDA LUGEDES PANE RAKENDUS MIINUSEST ALLA JA AVA UUESTI, MUIDU EI LASE NUMBREID SISESTADA")
    
    def toggle_history(self):
        # Toggle the state of the show/hide history button and update the history text widget
        if self.show_history_button["text"] == "Show History":
            self.show_history_button["text"] = "Hide History"
            self.c.execute("SELECT * FROM calculations")
            calc_history = [f"{row[0]} {row[2]} {row[1]} = {row[3]}" for row in self.c.fetchall()]
            for history_item in calc_history:
                self.history_text.insert(tk.END, history_item + "\n")
        else:
            self.show_history_button["text"] = "Show History"
            self.history_text.delete('1.0', tk.END)
            
    def delete_history(self):
    # Confirm with user before deleting all records
        if messagebox.askyesno("Delete History", "Kindel, et tahad tehete ajaloo ära kustutada?"):
            # Delete all records from the calculations table
            self.c.execute("DELETE FROM calculations")
            self.conn.commit()

            # Clear the history text widget
            self.history_text.delete('1.0', tk.END)


    def __del__(self):
        # Close the database connection when the object is destroyed
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    calc.show_help()
    root.mainloop()
