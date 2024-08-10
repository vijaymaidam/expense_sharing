import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database initialization
conn = sqlite3.connect('expenses.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, user_id INTEGER, description TEXT, amount REAL, date TEXT)''')
conn.commit()


def add_expense():
    user_id = user_id_entry.get()
    description = description_entry.get()
    amount = float(amount_entry.get())
    date = date_entry.get()

    c.execute("INSERT INTO expenses (user_id, description, amount, date) VALUES (?, ?, ?, ?)",
              (user_id, description, amount, date))
    conn.commit()

    messagebox.showinfo("Success", "Expense added successfully")


def split_bill():
    total_amount = float(total_amount_entry.get())
    num_people = int(num_people_entry.get())

    share_amount = total_amount / num_people

    messagebox.showinfo("Bill Split", f"Each person owes {share_amount:.2f}.")


def get_debts():
    user_id = int(user_id_debts_entry.get())
    c.execute("SELECT user_id, SUM(amount) FROM expenses WHERE user_id != ? GROUP BY user_id", (user_id,))
    debts = c.fetchall()

    message = "Debts:\n"
    for debt in debts:
        message += f"User {debt[0]} owes {debt[1]}.\n"

    messagebox.showinfo("Debts", message)


# GUI setup
root = tk.Tk()
root.title("Expense Manager")

# Add Expense
add_expense_frame = tk.Frame(root)
add_expense_frame.pack(pady=10)

user_id_label = tk.Label(add_expense_frame, text="User ID:")
user_id_label.grid(row=0, column=0)
user_id_entry = tk.Entry(add_expense_frame)
user_id_entry.grid(row=0, column=1)

description_label = tk.Label(add_expense_frame, text="Description:")
description_label.grid(row=1, column=0)
description_entry = tk.Entry(add_expense_frame)
description_entry.grid(row=1, column=1)

amount_label = tk.Label(add_expense_frame, text="Amount:")
amount_label.grid(row=2, column=0)
amount_entry = tk.Entry(add_expense_frame)
amount_entry.grid(row=2, column=1)

date_label = tk.Label(add_expense_frame, text="Date:")
date_label.grid(row=3, column=0)
date_entry = tk.Entry(add_expense_frame)
date_entry.grid(row=3, column=1)

add_expense_button = tk.Button(add_expense_frame, text="Add Expense", command=add_expense)
add_expense_button.grid(row=4, columnspan=2)

# Split Bill
split_bill_frame = tk.Frame(root)
split_bill_frame.pack(pady=10)

total_amount_label = tk.Label(split_bill_frame, text="Total Amount:")
total_amount_label.grid(row=0, column=0)
total_amount_entry = tk.Entry(split_bill_frame)
total_amount_entry.grid(row=0, column=1)

num_people_label = tk.Label(split_bill_frame, text="Number of People:")
num_people_label.grid(row=1, column=0)
num_people_entry = tk.Entry(split_bill_frame)
num_people_entry.grid(row=1, column=1)

split_bill_button = tk.Button(split_bill_frame, text="Split Bill", command=split_bill)
split_bill_button.grid(row=2, columnspan=2)

# Get Debts
get_debts_frame = tk.Frame(root)
get_debts_frame.pack(pady=10)

user_id_debts_label = tk.Label(get_debts_frame, text="User ID:")
user_id_debts_label.grid(row=0, column=0)
user_id_debts_entry = tk.Entry(get_debts_frame)
user_id_debts_entry.grid(row=0, column=1)

get_debts_button = tk.Button(get_debts_frame, text="Get Debts", command=get_debts)
get_debts_button.grid(row=1, columnspan=2)

root.mainloop()