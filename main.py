import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


# Function to add a product to the database
def add_product():
    date = date_entry.get()
    quantity = quantity_entry.get()
    product_name = product_entry.get()
    person_name = person_entry.get()
    payment_status = payment_status_var.get()

    if date and quantity and product_name and person_name:
        try:
            quantity = int(quantity)
            conn.execute(
                "INSERT INTO products (date, quantity, name, person, payment_status) VALUES (?, ?, ?, ?, ?)",
                (date, quantity, product_name, person_name, payment_status),
            )
            conn.commit()
            messagebox.showinfo("Success", "Product added successfully!")
            clear_entries()
            load_data()
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
    else:
        messagebox.showwarning("Warning", "Please fill in all fields.")


# Function to clear entry fields
def clear_entries():
    date_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    product_entry.delete(0, tk.END)
    person_entry.delete(0, tk.END)
    payment_status_var.set("Not Paid")  # Reset payment status to "Not Paid"


# Function to search for a product by name
def search_product():
    search_term = search_entry.get()
    if search_term:
        cursor.execute(
            "SELECT * FROM products WHERE name LIKE ? OR person LIKE ?",
            ("%" + search_term + "%", "%" + search_term + "%"),
        )
        rows = cursor.fetchall()
        display_data(rows)
    else:
        load_data()


# Function to show all data
def show_all_data():
    load_data()


# Function to load data into the treeview
def load_data():
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    display_data(rows)


# Function to display data in the treeview
def display_data(rows):
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", tk.END, values=row)


# Function to handle treeview selection
def on_select(event):
    selected_item = tree.selection()[0]
    selected_data = tree.item(selected_item, "values")

    # Display selected data in the details section
    details_label.config(text=f"Details for Product ID {selected_data[0]}:")
    details_text.config(state=tk.NORMAL)
    details_text.delete(1.0, tk.END)
    details_text.insert(tk.END, f"Date: {selected_data[1]}\n")
    details_text.insert(tk.END, f"Quantity: {selected_data[2]}\n")
    details_text.insert(tk.END, f"Product Name: {selected_data[3]}\n")
    details_text.insert(tk.END, f"Person: {selected_data[4]}\n")
    details_text.insert(tk.END, f"Payment Status: {selected_data[5]}\n")
    details_text.config(state=tk.DISABLED)

    # Enable edit and delete buttons
    edit_button.config(state=tk.NORMAL)
    delete_button.config(state=tk.NORMAL)


# Function to edit selected product
def edit_product():
    selected_item = tree.selection()[0]
    selected_data = tree.item(selected_item, "values")

    # Open a new window for editing
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Product")

    # Create and place widgets in the edit window
    date_label = tk.Label(edit_window, text="Date:")
    date_label.grid(row=0, column=0, padx=10, pady=10)

    date_entry_edit = tk.Entry(edit_window)
    date_entry_edit.insert(tk.END, selected_data[1])
    date_entry_edit.grid(row=0, column=1, padx=10, pady=10)

    quantity_label = tk.Label(edit_window, text="Quantity:")
    quantity_label.grid(row=1, column=0, padx=10, pady=10)

    quantity_entry_edit = tk.Entry(edit_window)
    quantity_entry_edit.insert(tk.END, selected_data[2])
    quantity_entry_edit.grid(row=1, column=1, padx=10, pady=10)

    product_label = tk.Label(edit_window, text="Product Name:")
    product_label.grid(row=2, column=0, padx=10, pady=10)

    product_entry_edit = tk.Entry(edit_window)
    product_entry_edit.insert(tk.END, selected_data[3])
    product_entry_edit.grid(row=2, column=1, padx=10, pady=10)

    person_label = tk.Label(edit_window, text="Person:")
    person_label.grid(row=3, column=0, padx=10, pady=10)

    person_entry_edit = tk.Entry(edit_window)
    person_entry_edit.insert(tk.END, selected_data[4])
    person_entry_edit.grid(row=3, column=1, padx=10, pady=10)

    payment_status_label = tk.Label(edit_window, text="Payment Status:")
    payment_status_label.grid(row=4, column=0, padx=10, pady=10)

    payment_status_combobox = ttk.Combobox(edit_window, values=("Not Paid", "Paid"))
    payment_status_combobox.set(selected_data[5])  # Set the current value
    payment_status_combobox.grid(row=4, column=1, padx=10, pady=10)

    update_button = tk.Button(
        edit_window,
        text="Update Product",
        command=lambda: update_product(
            selected_data[0],
            date_entry_edit.get(),
            quantity_entry_edit.get(),
            product_entry_edit.get(),
            person_entry_edit.get(),
            payment_status_combobox.get(),
            edit_window,
        ),
    )
    update_button.grid(row=5, column=0, columnspan=2, pady=10)


# Function to update product in the database
def update_product(
    product_id, date, quantity, product_name, person_name, payment_status, edit_window
):
    try:
        quantity = int(quantity)
        conn.execute(
            "UPDATE products SET date=?, quantity=?, name=?, person=?, payment_status=? WHERE id=?",
            (date, quantity, product_name, person_name, payment_status, product_id),
        )
        conn.commit()
        messagebox.showinfo("Success", "Product updated successfully!")
        edit_window.destroy()
        load_data()
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a number.")


# Function to delete selected product
def delete_product():
    result = messagebox.askyesno(
        "Delete Product", "Are you sure you want to delete this product?"
    )
    if result:
        selected_item = tree.selection()[0]
        selected_data = tree.item(selected_item, "values")
        conn.execute("DELETE FROM products WHERE id=?", (selected_data[0],))
        conn.commit()
        messagebox.showinfo("Success", "Product deleted successfully!")
        load_data()


# Create database and table
conn = sqlite3.connect("products.db")
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, date TEXT, quantity INTEGER, name TEXT, person TEXT, payment_status TEXT)"
)
conn.commit()

# Create the main window
root = tk.Tk()
root.geometry("1500x600")
root.title("Product Management System")

# Create and place widgets
date_label = tk.Label(root, text="Date:")
date_label.grid(row=0, column=0, padx=1, pady=1, sticky="e")

date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=1, pady=1, sticky="w")

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.grid(row=1, column=0, padx=1, pady=1, sticky="e")

quantity_entry = tk.Entry(root)
quantity_entry.grid(row=1, column=1, padx=1, pady=1, sticky="w")

product_label = tk.Label(root, text="Product Name:")
product_label.grid(row=2, column=0, padx=1, pady=1, sticky="e")

product_entry = tk.Entry(root)
product_entry.grid(row=2, column=1, padx=1, pady=1, sticky="w")

person_label = tk.Label(root, text="Person:")
person_label.grid(row=3, column=0, padx=1, pady=1, sticky="e")

person_entry = tk.Entry(root)
person_entry.grid(row=3, column=1, padx=1, pady=1, sticky="w")

payment_status_label = tk.Label(root, text="Payment Status:")
payment_status_label.grid(row=4, column=0, padx=1, pady=1, sticky="e")

payment_status_var = tk.StringVar(root)
payment_status_combobox = ttk.Combobox(
    root, textvariable=payment_status_var, values=("Not Paid", "Paid")
)
payment_status_combobox.set("Not Paid")
payment_status_combobox.grid(row=4, column=1, padx=10, pady=10, sticky="w")

add_button = tk.Button(root, text="Add Product", command=add_product)
add_button.grid(row=5, column=0, columnspan=2, pady=10)

search_label = tk.Label(root, text="Search:")
search_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")

search_entry = tk.Entry(root)
search_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

search_button = tk.Button(root, text="Search", command=search_product)
search_button.grid(row=7, column=0, pady=10, sticky="e")

show_all_button = tk.Button(root, text="Show All", command=show_all_data)
show_all_button.grid(row=7, column=1, pady=10, sticky="w")

# Create treeview to display data
tree = ttk.Treeview(
    root, columns=("ID", "Date", "Quantity", "Product Name", "Person", "Payment Status")
)
tree.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky="nsew")
tree.heading("#0", text="ID")
tree.heading("#1", text="Date")
tree.heading("#2", text="Quantity")
tree.heading("#3", text="Product Name")
tree.heading("#4", text="Person")
tree.heading("#5", text="Payment Status")
tree.bind("<ButtonRelease-1>", on_select)


# Create a section for details
details_label = tk.Label(root, text="Details:", width=10)
details_label.grid(row=8, column=2, pady=0, sticky="w")

details_text = tk.Text(
    root, height=10, width=10, state=tk.DISABLED
)  # Creates a tkinter Text widget to display product details
# Disabled by default until a product is selected

details_text.grid(row=9, column=2, columnspan=1, padx=1, pady=1, sticky="nsew")

# Add Edit and Delete buttons

edit_button = tk.Button(
    root, text="Edit Product", command=edit_product, state=tk.DISABLED
)
edit_button.grid(row=10, column=1, pady=5, sticky="e")

delete_button = tk.Button(
    root, text="Delete Product", command=delete_product, state=tk.DISABLED
)
delete_button.grid(row=10, column=2, pady=10, sticky="w")

# Configure row and column weights to make the treeview expand with the window
root.grid_rowconfigure(8, weight=1)
root.grid_columnconfigure(2, weight=1)

load_data()

# Run the main loop
root.mainloop()
