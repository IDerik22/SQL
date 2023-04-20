from tkinter import ttk
import tkinter as tk
from ttkbootstrap import Style
import pandas as pd
import sqlite3

# Connect to the SQLite3 database
conn = sqlite3.connect('C:\sqlite\epood_eteppan;')

# Load data from a SQLite3 table
df = pd.read_sql_query("SELECT * FROM eteppan", conn)

def update_treeview():
    # Clear previous data from the treeview
    treeview.delete(*treeview.get_children())

    # Get the current page and rows per page values
    global current_page
    global rows_per_page
    start_row = (current_page - 1) * rows_per_page
    end_row = start_row + rows_per_page - 1

    # Get the search term from the search entry widget
    search_term = search_entry.get()

    # Get the data from the dataframe and insert it into the treeview
    if search_term:
        for row in df[df.apply(lambda x: x.astype(str).str.contains(search_term, case=False).any(), axis=1)].iloc[start_row:end_row].itertuples():
            treeview.insert('', 'end', values=row[1:])
    else:
        for row in df.iloc[start_row:end_row].itertuples():
            treeview.insert('', 'end', values=row[1:])


def change_rows_per_page(value):
    # Update the rows per page value and update the treeview
    global rows_per_page
    rows_per_page = int(value)
    update_treeview()
    update_page_label()

def change_page(value):
    # Update the current page value and update the treeview
    global current_page
    current_page = int(value)
    update_treeview()
    update_page_label()

def update_page_label():
    # Update the page label with the current page number
    page_label.configure(text='Page ' + str(current_page))
    
def search():
    # Clear previous data from the treeview
    treeview.delete(*treeview.get_children())

    # Get the search term from the search entry widget
    search_term = search_entry.get()

    # Get the data from the dataframe that matches the search term and insert it into the treeview
    for row in df[df.apply(lambda x: x.astype(str).str.contains(search_term, case=False).any(), axis=1)].itertuples():
        treeview.insert('', 'end', values=row[1:])


# Set the initial rows per page and current page values
rows_per_page = 10
current_page = 1

# Create the main window
root = tk.Tk()
root.title('Data Viewer')

# Create a frame for the scale widgets
scale_frame = ttk.Frame(root)
scale_frame.grid(row=0, column=0, padx=5, pady=5)

# Create a scale widget for selecting the rows per page
rows_label = ttk.Label(scale_frame, text='Rows per page:')
rows_label.pack(side=tk.LEFT, padx=5, pady=5)

rows_per_page_entry = ttk.Entry(scale_frame, width=5)
rows_per_page_entry.insert(0, rows_per_page)
rows_per_page_entry.pack(side=tk.LEFT)

rows_button = ttk.Button(scale_frame, text="Update", command=lambda: change_rows_per_page(rows_per_page_entry.get()))
rows_button.pack(side=tk.LEFT, padx=5)

# Create a scale widget for selecting the current page
page_label = ttk.Label(root, text='Page ' + str(current_page))
page_label.grid(row=1, column=0, padx=5, pady=5)

page_entry = ttk.Entry(root, width=5)
page_entry.insert(0, current_page)
page_entry.grid(row=1, column=1)

page_button = ttk.Button(root, text="Go to page", command=lambda: change_page(page_entry.get()))
page_button.grid(row=1, column=2, padx=5)

# Create a frame for the search widget
search_frame = ttk.Frame(root)
search_frame.grid(row=0, column=1, padx=5, pady=5)

# Create a search entry widget
search_entry = ttk.Entry(search_frame, width=20)
search_entry.pack(side=tk.LEFT)

# Create a search button
search_button = ttk.Button(search_frame, text='Search', command=search)
search_button.pack(side=tk.LEFT, padx=5)


# Create the treeview widget
columns = df.columns.tolist()
treeview = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    treeview.heading(col, text=col)
treeview.grid(row=2, column=0, columnspan=len(columns), padx=5, pady=5, sticky='nsew')
update_treeview()

# Start the main event loop
root.mainloop()

# Close the SQLite3 connection
conn.close()