   
from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
DB_NAME = "bank.db"
def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            account_number INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp TEXT NOT NULL,
            receiver_account INTEGER
        )
    """)
    conn.commit()
    conn.close()
init_database()
def start_gui():
    root = tk.Tk()
    root.title("Bank Management System")
    root.geometry("700x650")
    root.resizable(True,True)
    root.configure(bg="#eef3f8")
    root.state("zoomed")
    bank = Bank()
    

    title = tk.Label(
        root,
        text="BANK MANAGEMENT SYSTEM",
        font=("Arial", 20, "bold"),
        bg= "#eef3f8",
        fg="#17365D"
    )
    title.pack(pady=30)

    subtitle = tk.Label(
        root,
        text="Welcome to your banking system",
        font=("Arial", 12),
        bg= "#eef3f8",
        fg="#555555"
    )
    subtitle.pack(pady=10)
    button_frame = tk.Frame(
        root,
        bg="#f2f5f9"
    )
    button_frame.pack(pady=20)
    button_width = 22
    button_height = 2
    button_font = ("Arial",12,"bold")
    button_bg = "#1f4e78"
    button_fg = "white"

    def create_account_gui():
        name = simpledialog.askstring(
            "Create Account",
            "Enter customer name:",
            parent=root
        )

        if name is None:
            return

        name = name.strip()

        if not name:
            messagebox.showerror(
                "Invalid Name",
                "Customer name cannot be empty."
            )
            return

        balance = simpledialog.askfloat(
            "Create Account",
            "Enter initial balance:",
            parent=root,
            minvalue=0
        )

        if balance is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            # Generate new account number
            cursor.execute(
                """
                SELECT MAX(account_number)
                FROM accounts
                """
            )

            result = cursor.fetchone()

            if result[0] is None:
                account_number = 1001
            else:
                account_number = result[0] + 1

            # Create account
            cursor.execute(
                """
                INSERT INTO accounts
                (account_number, name, balance)
                VALUES (?, ?, ?)
                """,
                (
                    account_number,
                    name,
                    balance
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Account Created",
                f"Account created successfully!\n\n"
                f"Customer: {name}\n"
                f"Account Number: {account_number}\n"
                f"Initial Balance: ₹{balance:,.2f}"
            )

        except sqlite3.Error as e:
            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    def check_balance_gui():
        account_number = simpledialog.askinteger(
            "Check Balance",
            "Enter account number:",
            parent=root,
            minvalue=1
        )

        if account_number is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                messagebox.showerror(
                    "Account Not Found",
                    "This account number does not exist."
                )
            else:
                messagebox.showinfo(
                    "Account Balance",
                    f"Customer: {account[0]}\n"
                    f"Account Number: {account_number}\n"
                    f"Balance: ₹{account[1]:,.2f}"
                )

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    
    def deposit_money_gui():
        account_number = simpledialog.askinteger(
            "Deposit Money",
            "Enter account number:",
            parent=root,
            minvalue=1
        )

        if account_number is None:
            return

        amount = simpledialog.askfloat(
            "Deposit Money",
            "Enter deposit amount:",
            parent=root,
            minvalue=0.01
        )

        if amount is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                messagebox.showerror(
                    "Account Not Found",
                    "This account number does not exist."
                )
                return

            new_balance = account[1] + amount

            transaction_id = bank.generate_transaction_id()
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (new_balance, account_number)
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number,
                 transaction_type, amount, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    transaction_id,
                    account_number,
                    "Deposit",
                    amount,
                    timestamp
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Deposit Successful",
                f"Customer: {account[0]}\n"
                f"Deposited: ₹{amount:,.2f}\n"
                f"New Balance: ₹{new_balance:,.2f}\n"
                f"Transaction ID: {transaction_id}"
            )

        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    def withdraw_money_gui():
        account_number = simpledialog.askinteger(
            "Withdraw Money",
            "Enter account number:",
            parent=root,
            minvalue=1
        )

        if account_number is None:
            return

        amount = simpledialog.askfloat(
            "Withdraw Money",
            "Enter withdrawal amount:",
            parent=root,
            minvalue=0.01
        )

        if amount is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                messagebox.showerror(
                    "Account Not Found",
                    "This account number does not exist."
                )
                return

            if amount > account[1]:
                messagebox.showerror(
                    "Insufficient Balance",
                    f"Available Balance: ₹{account[1]:,.2f}"
                )
                return

            new_balance = account[1] - amount

            transaction_id = bank.generate_transaction_id()
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (new_balance, account_number)
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number,
                 transaction_type, amount, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    transaction_id,
                    account_number,
                    "Withdraw",
                    amount,
                    timestamp
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Withdrawal Successful",
                f"Customer: {account[0]}\n"
                f"Withdrawn: ₹{amount:,.2f}\n"
                f"New Balance: ₹{new_balance:,.2f}\n"
                f"Transaction ID: {transaction_id}"
            )

        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    def transfer_money_gui():
        from_account = simpledialog.askinteger(
            "Transfer Money",
            "Enter sender account number:",
            parent=root,
            minvalue=1
        )

        if from_account is None:
            return

        to_account = simpledialog.askinteger(
            "Transfer Money",
            "Enter receiver account number:",
            parent=root,
            minvalue=1
        )

        if to_account is None:
            return

        if from_account == to_account:
            messagebox.showerror(
                "Invalid Transfer",
                "Sender and receiver account cannot be same."
            )
            return

        amount = simpledialog.askfloat(
            "Transfer Money",
            "Enter transfer amount:",
            parent=root,
            minvalue=0.01
        )

        if amount is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            # Sender
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (from_account,)
            )
            sender = cursor.fetchone()

            if sender is None:
                messagebox.showerror(
                    "Error",
                    "Sender account not found."
                )
                return

            # Receiver
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (to_account,)
            )
            receiver = cursor.fetchone()

            if receiver is None:
                messagebox.showerror(
                    "Error",
                    "Receiver account not found."
                )
                return

            if amount > sender[1]:
                messagebox.showerror(
                    "Insufficient Balance",
                    f"Available Balance: ₹{sender[1]:,.2f}"
                )
                return

            # New receiver check
            cursor.execute(
                """
                SELECT 1
                FROM transactions
                WHERE transaction_type = 'Transfer money'
                  AND (
                      (account_number = ? AND receiver_account = ?)
                      OR
                      (account_number = ? AND receiver_account = ?)
                  )
                LIMIT 1
                """,
                (
                    from_account,
                    to_account,
                    to_account,
                    from_account
                )
            )

            previous_transfer = cursor.fetchone()

            if previous_transfer is None:
                result = messagebox.askyesno(
                    "New Receiver Warning",
                    f"Receiver: {receiver[0]}\n"
                    f"Account: {to_account}\n\n"
                    "You have not transferred between these accounts before.\n\n"
                    "Do you want to continue?"
                )

                if not result:
                    return

            # High-value warning
            if amount >= 10000:
                result = messagebox.askyesno(
                    "High-Value Transfer Warning",
                    f"Receiver: {receiver[0]}\n"
                    f"Amount: ₹{amount:,.2f}\n\n"
                    "This is a high-value transfer.\n\n"
                    "Do you want to continue?"
                )

                if not result:
                    return

            # Final confirmation
            result = messagebox.askyesno(
                "Confirm Transfer",
                f"Sender: {sender[0]}\n"
                f"Sender Account: {from_account}\n\n"
                f"Receiver: {receiver[0]}\n"
                f"Receiver Account: {to_account}\n\n"
                f"Amount: ₹{amount:,.2f}\n\n"
                "Confirm this transfer?"
            )

            if not result:
                return

            sender_new_balance = sender[1] - amount
            receiver_new_balance = receiver[1] + amount

            transaction_id = bank.generate_transaction_id()

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Update sender
            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (sender_new_balance, from_account)
            )

            # Update receiver
            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (receiver_new_balance, to_account)
            )

            # Sender transaction
            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number,
                 transaction_type, amount, timestamp,
                 receiver_account)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction_id,
                    from_account,
                    "Transfer money",
                    amount,
                    timestamp,
                    to_account
                )
            )

            # Receiver transaction
            receiver_transaction_id = transaction_id + "-R"

            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number,
                 transaction_type, amount, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    receiver_transaction_id,
                    to_account,
                    "Received money",
                    amount,
                    timestamp
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Transfer Successful",
                f"Transaction ID: {transaction_id}\n\n"
                f"Sender: {sender[0]}\n"
                f"Receiver: {receiver[0]}\n"
                f"Amount: ₹{amount:,.2f}\n\n"
                f"New Sender Balance: ₹{sender_new_balance:,.2f}"
            )

        except sqlite3.Error as e:
            conn.rollback()
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    def delete_account_gui():
        account_number = simpledialog.askinteger(
            "Delete Account",
            "Enter account number:",
            parent=root,
            minvalue=1
        )

        if account_number is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                messagebox.showerror(
                    "Account Not Found",
                    "This account number does not exist."
                )
                return

            confirmation = messagebox.askyesno(
                "Confirm Delete",
                f"Customer: {account[0]}\n"
                f"Account Number: {account_number}\n"
                f"Balance: ₹{account[1]:,.2f}\n\n"
                "Are you sure you want to delete this account?"
            )

            if not confirmation:
                return

            cursor.execute(
                """
                DELETE FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            conn.commit()

            messagebox.showinfo(
                "Account Deleted",
                f"Account {account_number} deleted successfully."
            )

        except sqlite3.Error as e:
            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    def update_name_gui():
        account_number = simpledialog.askinteger(
            "Update Customer Name",
            "Enter account number:",
            parent=root,
            minvalue=1
        )

        if account_number is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT name
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                messagebox.showerror(
                    "Account Not Found",
                    "This account number does not exist."
                )
                return

            new_name = simpledialog.askstring(
                "Update Customer Name",
                f"Current Name: {account[0]}\n\n"
                "Enter new customer name:",
                parent=root
            )

            if new_name is None:
                return

            new_name = new_name.strip()

            if not new_name:
                messagebox.showerror(
                    "Invalid Name",
                    "Customer name cannot be empty."
                )
                return

            cursor.execute(
                """
                UPDATE accounts
                SET name = ?
                WHERE account_number = ?
                """,
                (new_name, account_number)
            )

            conn.commit()

            messagebox.showinfo(
                "Name Updated",
                f"Customer name updated successfully!\n\n"
                f"New Name: {new_name}\n"
                f"Account Number: {account_number}"
            )

        except sqlite3.Error as e:
            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    def display_accounts_gui():
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT account_number, name, balance
                FROM accounts
                ORDER BY account_number
                """
            )

            accounts = cursor.fetchall()

            if not accounts:
                messagebox.showinfo(
                    "Accounts",
                    "No accounts found."
                )
                return

            account_text = "========== ALL ACCOUNTS ==========\n\n"

            for account in accounts:
                account_text += (
                    f"Account Number: {account[0]}\n"
                    f"Customer Name: {account[1]}\n"
                    f"Balance: ₹{account[2]:,.2f}\n"
                    "--------------------------------\n"
                )

            messagebox.showinfo(
                "All Accounts",
                account_text
            )

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    def search_account_gui():
        account_number = simpledialog.askinteger(
            "Search Account",
            "Enter account number:",
            parent=root,
            minvalue=1
        )

        if account_number is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT account_number, name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                messagebox.showerror(
                    "Account Not Found",
                    "This account number does not exist."
                )
            else:
                messagebox.showinfo(
                    "Account Found",
                    f"Account Number: {account[0]}\n"
                    f"Customer Name: {account[1]}\n"
                    f"Balance: ₹{account[2]:,.2f}"
                )

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    def transaction_history_gui():
        account_number = simpledialog.askinteger(
            "Transaction History",
            "Enter account number:",
            parent=root,
            minvalue=1
        )

        if account_number is None:
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT name
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                messagebox.showerror(
                    "Account Not Found",
                    "This account number does not exist."
                )
                return

            cursor.execute(
                """
                SELECT
                    t.transaction_id,
                    t.transaction_type,
                    t.amount,
                    t.timestamp,
                    t.receiver_account,
                    r.name
                FROM transactions t
                LEFT JOIN accounts r
                    ON t.receiver_account = r.account_number
                WHERE t.account_number = ?
                ORDER BY t.timestamp DESC
                """,
                (account_number,)
            )

            transactions = cursor.fetchall()

            if not transactions:
                messagebox.showinfo(
                    "Transaction History",
                    f"Customer: {account[0]}\n\n"
                    "No transactions found."
                )
                return

            history = (
                f"Customer: {account[0]}\n"
                f"Account Number: {account_number}\n\n"
                "========== TRANSACTIONS ==========\n\n"
            )

            for transaction in transactions:
                history += (
                    f"Transaction ID: {transaction[0]}\n"
                    f"Type: {transaction[1]}\n"
                    f"Amount: ₹{transaction[2]:,.2f}\n"
                    f"Date & Time: {transaction[3]}\n"
                )

                if transaction[4] is not None:
                    history += (
                        f"Receiver Account: {transaction[4]}\n"
                        f"Receiver Name: {transaction[5]}\n"
                    )

                history += "\n------------------------------\n"

            # Create transaction history window
            history_window = tk.Toplevel(root)
            history_window.title("Transaction History")
            history_window.geometry("650x600")
            history_window.configure(bg="#eef3f8")

            # Heading
            history_title = tk.Label(
                history_window,
                text="TRANSACTION HISTORY",
                font=("Arial", 18, "bold"),
                bg="#eef3f8",
                fg="#17365D"
            )
            history_title.pack(pady=15)

            # Frame for text and scrollbar
            history_frame = tk.Frame(
                history_window,
                bg="#eef3f8"
            )
            history_frame.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=10
            )

            # Scrollbar
            scrollbar = tk.Scrollbar(
                history_frame
            )
            scrollbar.pack(
                side="right",
                fill="y"
            )

            # Text area
            history_text = tk.Text(
                history_frame,
                font=("Arial", 11),
                wrap="word",
                yscrollcommand=scrollbar.set
            )
            history_text.pack(
                side="left",
                fill="both",
                expand=True
            )

            scrollbar.config(
                command=history_text.yview
            )

            # Insert history
            history_text.insert(
                "1.0",
                history
            )

            # Make text read-only
            history_text.config(
                state="disabled"
            )

            # Close button
            close_button = tk.Button(
                history_window,
                text="Close",
                font=("Arial", 11, "bold"),
                width=15,
                bg="#8B0000",
                fg="white",
                command=history_window.destroy
            )
            close_button.pack(pady=15)

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            conn.close()
    create_button = tk.Button(
        button_frame,
        text="Create Account",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=create_account_gui
    )
    create_button.grid(row=0,column=0,padx=10,pady=10)
    balance_button = tk.Button(
            button_frame,
            text="Check Balance",
            font= button_font,
            width=button_width,
            height= button_height,
            bg= button_bg,
            fg=button_fg,
            
            command=check_balance_gui
        )
    balance_button.grid(row=0,column=1,padx=10,pady=10)
    deposit_button = tk.Button(
        button_frame,
        text="Deposit Money",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=deposit_money_gui
    )
    deposit_button.grid(row=1,column=0,padx=10,pady=10)
    withdraw_button = tk.Button(
        button_frame,
        text="Withdraw Money",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=withdraw_money_gui
    )
    withdraw_button.grid(row=1,column=1,padx=10,pady=10)
    transfer_button = tk.Button(
        button_frame,
        text="Transfer Money",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=transfer_money_gui
    )
    transfer_button.grid(row=2,column=0,padx=10,pady=10)
    delete_button = tk.Button(
        button_frame,
        text="Delete Account",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=delete_account_gui
    )
    delete_button.grid(row=2,column=1,padx=10,pady=10)
    update_name_button = tk.Button(
        button_frame,
        text="Update Customer Name",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=update_name_gui
    )
    update_name_button.grid(row=3,column=0,padx=10,pady=10)
    display_button = tk.Button(
        button_frame,
        text="Display All Accounts",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=display_accounts_gui
    )
    display_button.grid(row=3,column=1,padx=10,pady=10)
    search_button = tk.Button(
        button_frame,
        text="Search Account",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=search_account_gui
    )
    search_button.grid(row=4,column=0,padx=10,pady=10)
    history_button = tk.Button(
        button_frame,
        text="Transaction History",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= button_bg,
        fg=button_fg,
        command=transaction_history_gui
    )
    history_button.grid(row=4,column=1,padx=10,pady=10)
    exit_button = tk.Button(
        button_frame,
        text="Exit",
        font= button_font,
        width=button_width,
        height= button_height,
        bg= "#8B0000",
        fg="white",
        command=root.destroy
    )
    exit_button.grid(row=6,column=0,columnspan=2,padx=10,pady=15)
    root.mainloop()
# ==========================================================
# BANK CLASS
# ==========================================================
class Bank:
    def __init__(self):   
        self.transaction_counter = 1000
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT transaction_id
        FROM transactions
        WHERE transaction_id LIKE 'TXN%'
          AND transaction_id NOT LIKE '%-R'
        ORDER BY CAST(SUBSTR(transaction_id, 4) AS INTEGER) DESC
        LIMIT 1
    """)      
        last_transaction = cursor.fetchone()
    
        if last_transaction:
            last_id = last_transaction[0]
            try:
                self.transaction_counter = int(
                    last_id.replace("TXN", "")
                )
            except ValueError:
                self.transaction_counter = 1000
        conn.close()
    # ======================================================
    # TRANSACTION ID
    # =====================================================
    def generate_transaction_id(self):
        self.transaction_counter += 1
        return f"TXN{self.transaction_counter}"
    # ======================================================
    # ACCOUNT NUMBER INPUT
    # ======================================================
    @staticmethod
    def get_account_number():
        while True:
            try:
                account_number = int(
                    input("Enter the account number: ")
                )
                if account_number <= 0:
                    print(
                        "Account number must be greater than 0"
                    )
                    continue
                return account_number
            except ValueError:
                print(
                    "Please enter a valid account number"
                )
    # ======================================================
    # CREATE ACCOUNT
    # ======================================================
    def create_account(self):
        conn = sqlite3.connect(DB_NAME) 
        cursor = conn.cursor()
        try:
            account_number = self.get_account_number()
            name = input("Enter the account holder name :").strip()
            if not name:
                print("Name cannot be empty")
                return
            balance = float(input("Enter the initial balance :"))
            if balance < 0:
                print("Balance cannot be a negative")
                return
            cursor.execute("""
              INSERT INTO accounts
              (account_number ,name,balance)
              VALUES(?,?,?)"""
             ,(account_number,name,balance)
            )
            conn.commit()
            print("\nAccount  created successfully!")
            print("Account Number :",account_number)
        except ValueError:
            print("Please  enter a valid amount")
        except sqlite3.IntegrityError:
            print("Account number already exists.")
        finally:
            conn.close()
    # ======================================================
    # DEPOSIT MONEY
    # ======================================================
    def deposit_money(self):
        print("================DEPOSIT MONEY==================")
        account_number = self.get_account_number()
        conn =  sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT name,balance FROM accounts 
            WHERE account_number =?""",(account_number,))
            account = cursor.fetchone()
            if account is None:
                print("Account is not a found")
                return
            try:
                amount = int(input("Enter the amount:"))
            except ValueError:
                print("please enter the valid  amount")
                return
            if amount <= 0:
                print("Amount must be greater than zero ")
                return
            new_balance = account[1]+amount
            transaction_id = self.generate_transaction_id()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                """
                UPDATE accounts
                SET balance =?
                WHERE account_number =?""",
                (new_balance,account_number)
            )
            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id,account_number,
                transaction_type,amount,timestamp)
                VALUES(?,?,?,?,?)""",
                (
                    transaction_id,
                    account_number,
                    "Deposit",
                    amount,
                    timestamp
                )
            )
            conn.commit()
            print("\nCustomer Name :",account[0])
            print("Deposited :",amount)
            print("New Balance :",new_balance)
            print("Transaction ID :",transaction_id)
            print("\n money deposited successfully")
        except sqlite3.Error as e:
            conn.rollback()   
            print("Database error:",e)
        finally:
            conn.close()
    # ======================================================
    # WITHDRAW MONEY
    # ======================================================
    def withdraw_money(self):

        print("\n========== WITHDRAW MONEY ==========")
    
        account_number = self.get_account_number()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT name, balance FROM accounts WHERE account_number = ?",
                (account_number,)
            )
            account = cursor.fetchone()
            if account is None:
                print("Account is not found.")
                return
            try:
                amount = int(
                    input("Enter the withdraw amount: ")
                )
            except ValueError:
                print("Please enter a valid amount.")
                return
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
            if amount > account[1]:
                print("Insufficient balance.")
                return
            new_balance = account[1] - amount
            transaction_id = self.generate_transaction_id()    
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )    
            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (new_balance, account_number)
            )
    
            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number,
                 transaction_type, amount, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    transaction_id,
                    account_number,
                    "Withdraw",
                    amount,
                    timestamp
                )
            )
    
            conn.commit()
    
            print("\nCustomer Name :", account[0])
            print("Withdrawn     :", amount)
            print("New Balance   :", new_balance)
            print("Transaction ID:", transaction_id)
            print("Date & Time   :", timestamp)
    
            print("\nMoney withdrawn successfully.")
    
        except sqlite3.Error as e:
            conn.rollback()
            print("Database error:", e)
    
        finally:
            conn.close()
    # ======================================================
    # CHECK BALANCE
    # ======================================================
    def check_balance(self):

        print("\n========== CHECK BALANCE ==========")
    
        account_number = self.get_account_number()
    
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
    
        try:
    
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )
    
            account = cursor.fetchone()
    
            if account is None:
                print("Account is not found.")
                return
    
            print("\nCustomer Name :", account[0])
            print("Account Number:", account_number)
            print("Current Balance:", account[1])
    
        except sqlite3.Error as e:
            print("Database error:", e)
    
        finally:
            conn.close()
    # ======================================================
    # DISPLAY ALL ACCOUNTS
    # ======================================================
    def display_accounts(self):

        print("\n========== ALL ACCOUNTS ==========")
    
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
    
        try:
            cursor.execute("""
                SELECT account_number, name, balance
                FROM accounts
                ORDER BY account_number
            """)
    
            accounts = cursor.fetchall()
    
            if not accounts:
                print("No accounts found.")
                return
    
            for account in accounts:
                print("---------------------------------------------")
                print("Account Number :", account[0])
                print("Customer Name  :", account[1])
                print("Balance        :", account[2])
    
            print("---------------------------------------------")
    
        except sqlite3.Error as e:
            print("Database error:", e)
    
        finally:
            conn.close()
    # ======================================================
    # DELETE ACCOUNT
    # ======================================================
    def delete_account(self):
        print("\n========== DELETE ACCOUNT ==========")
        account_number = self.get_account_number()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT name
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )
    
            account = cursor.fetchone()
    
            if account is None:
                print("Account not found.")
                return
    
            print("Customer Name:", account[0])
    
            confirm = input(
                "Are you sure you want to delete this account? (yes/no): "
            ).strip().lower()
    
            if confirm != "yes":
                print("Account deletion cancelled.")
                return
    
            cursor.execute(
                """
                DELETE FROM transactions
                WHERE account_number = ?
                """,
                (account_number,)
            )
            cursor.execute(
                """
                DELETE FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )
            conn.commit()
            print("\nAccount deleted successfully!")
        except sqlite3.Error as e:
            conn.rollback()
            print("Database error:", e)
        finally:
            conn.close()
    # ======================================================
    # UPDATE CUSTOMER NAME
    # ======================================================
    def update_name(self):
        print("\n========== UPDATE NAME ==========")
        account_number = self.get_account_number()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT name
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )
            account = cursor.fetchone()
            if account is None:
                print("Account not found.")
                return
            print("Current Name:", account[0])
            new_name = input("Enter new name: ").strip()
            if not new_name:
                print("Name cannot be empty.")
                return
            cursor.execute(
                """
                UPDATE accounts
                SET name = ?
                WHERE account_number = ?
                """,
                (new_name, account_number)
            )    
            conn.commit()
    
            print("\nName updated successfully!")
            print("New Name:", new_name)    
        except sqlite3.Error as e:
            conn.rollback()
            print("Database error:", e)
        finally:
            conn.close()
    # ======================================================
    # TRANSFER MONEY
    # ======================================================
    def transfer_money(self):
        print("\n========== TRANSFER MONEY ==========")
        try:
            from_account_number = self.get_account_number()
            to_account_number = self.get_account_number()
        except ValueError:
            print("Please enter a valid account number.")
            return
        if from_account_number == to_account_number:
            print("Sender and receiver account cannot be same.")
            return
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            # Get sender
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (from_account_number,)
            )
            sender = cursor.fetchone()
            if sender is None:
                print("Sender account not found.")
                return
            # Get receiver
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (to_account_number,)
            )
            receiver = cursor.fetchone()
            if receiver is None:
                print("Receiver account not found.")
                return
            try:
                amount = int(
                    input("Enter the amount: ")
                )
            except ValueError:
                print("Please enter a valid amount.")
                return
            if amount <= 0:
                print("Invalid amount.")
                return
            if amount > sender[1]:
                print("Insufficient balance.")
                return
            # Check whether these two accounts have transferred before
            cursor.execute(
                """
                SELECT 1
                FROM transactions
                WHERE transaction_type = 'Transfer money'
                  AND (
                      (account_number = ? AND receiver_account = ?)
                      OR
                      (account_number = ? AND receiver_account = ?)
                  )
                LIMIT 1
                """,
                (
                    from_account_number,
                    to_account_number,
                    to_account_number,
                    from_account_number
                )
            )
            
            previous_transfer = cursor.fetchone()
            
            if previous_transfer is None:
                print("\n⚠️ NEW RECEIVER WARNING")
                print("---------------------------------------------")
                print("Receiver        :", receiver[0])
                print("Receiver Account:", to_account_number)
                print("You have not transferred between these accounts before.")
                print("---------------------------------------------")
            
                confirmation = input("Do you want to continue? (yes/no): ")
            
                if confirmation.lower() != "yes":
                    print("Transfer cancelled.")
                    return
            if amount >= 10000:
                print("\n⚠️ HIGH-VALUE TRANSFER WARNING")
                print("---------------------------------------------")
                print("Receiver        :", receiver[0])
                print("Receiver Account:", to_account_number)
                print("Transfer Amount :", amount)
                print("---------------------------------------------")
            
                confirmation = input("Do you want to continue? (yes/no): ")
            
                if confirmation.lower() != "yes":
                    print("Transfer cancelled.")
                    return
            # Final transfer confirmation
            print("\n========== TRANSFER SUMMARY ==========")
            print("Sender          :", sender[0])
            print("Sender Account  :", from_account_number)
            print("Receiver        :", receiver[0])
            print("Receiver Account:", to_account_number)
            print("Amount          :", amount)
            print("---------------------------------------------")
            
            confirmation = input("Confirm transfer? (yes/no): ")
            
            if confirmation.lower() != "yes":
                print("Transfer cancelled.")
                return
            # New balances
            sender_new_balance = sender[1] - amount
            receiver_new_balance = receiver[1] + amount
            # Generate transaction ID
            transaction_id = self.generate_transaction_id()
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            # Update sender balance
            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (sender_new_balance, from_account_number)
            )
    
            # Update receiver balance
            cursor.execute(
                """
                UPDATE accounts
                SET balance = ?
                WHERE account_number = ?
                """,
                (receiver_new_balance, to_account_number)
            )
    
            # Sender transaction
            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number,
                 transaction_type, amount, timestamp,
                 receiver_account)
                VALUES (?, ?, ?, ?, ?,?)
                """,
                (
                    transaction_id,
                    from_account_number,
                    "Transfer money",
                    amount,
                    timestamp,
                    to_account_number

                )
            )
            # Receiver transaction
            receiver_transaction_id = transaction_id + "-R"
            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number,
                 transaction_type, amount, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    receiver_transaction_id,
                    to_account_number,
                    "Received money",
                    amount,
                    timestamp
                )
            )
            conn.commit()
            print("\nMoney transferred successfully!")
            print("---------------------------------------------")
            print("Transaction ID :", transaction_id)
            print("Sender          :", sender[0])
            print("Sender Account  :", from_account_number)
            print("Sender Balance  :", sender_new_balance)
            print("---------------------------------------------")
            print("Receiver        :", receiver[0])
            print("Receiver Account:", to_account_number)
            print("Receiver Balance:", receiver_new_balance)
            print("---------------------------------------------")
            print("Transferred     :", amount)
            print("Date & Time     :", timestamp)
        except sqlite3.Error as e:
            conn.rollback()
            print("Database error:", e)
        finally:
            conn.close()
    # ======================================================
    # SEARCH ACCOUNT
    # ======================================================
    def search_accounts(self):
        print("\n========== SEARCH ACCOUNT ==========")
        account_number = self.get_account_number()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT account_number, name, balance
                FROM accounts
                WHERE account_number = ?
            """, (account_number,))
    
            account = cursor.fetchone()
    
            if account is None:
                print("Account not found.")
                return
            print("\nAccount found successfully!")
            print("---------------------------------------------")
            print("Account Number :", account[0])
            print("Customer Name  :", account[1])
            print("Balance        :", account[2])
            print("---------------------------------------------")
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            conn.close()
    # ======================================================
    # TRANSACTION HISTORY
    # ======================================================
    def transaction_history(self):
        print("\n========== TRANSACTION HISTORY ==========")
    
        account_number = self.get_account_number()
    
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
    
        try:
            # Get account details
            cursor.execute(
                """
                SELECT name, balance
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )
    
            account = cursor.fetchone()
    
            if account is None:
                print("This account is not found.")
                return
    
            print("Customer Name :", account[0])
            print("Account Number:", account_number)
    
            # Get transactions
            cursor.execute(
                """
                SELECT t.transaction_id,
                       t.transaction_type,
                       t.amount,
                       t.timestamp,
                       t.receiver_account,
                       a.name
                FROM transactions t
                LEFT JOIN accounts a
                ON t.receiver_account = a.account_number
                WHERE t.account_number = ?
                ORDER BY t.ROWID
                """,
                (account_number,)
            )
    
            transactions = cursor.fetchall()
    
            if not transactions:
                print("No transaction history found.")
                return
    
            print("---------------------------------------------")
    
            for transaction in transactions:
                print("Transaction ID :", transaction[0])
                print("Type            :", transaction[1])
                print("Amount          :", transaction[2])
                print("Date & Time     :", transaction[3])
    
                if transaction[4] is not None:
                    print("Receiver Account:", transaction[4])
                    print("Receiver Name   :", transaction[5])
    
                print("---------------------------------------------")
    
        except sqlite3.Error as e:
            print("Database error:", e)
    
        finally:
            conn.close()
    # ======================================================
    # MAIN MENU
    # ======================================================
    def run(self):
        while True:
            print("\n")
            print("=" * 50)
            print("          BANK MANAGEMENT SYSTEM")
            print("=" * 50)
            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check Balance")
            print("5. Display All Accounts")
            print("6. Delete Account")
            print("7. Update Customer Name")
            print("8. Transfer Money")
            print("9. Search Account")
            print("10. Transaction History")
            print("11. Exit")
            print("=" * 50)
            try:
                choice = int(
                    input("Enter your choice: ")
                )
            except ValueError:
                print("Please enter a valid choice.")
                continue
            if choice == 1:
                self.create_account()
            elif choice == 2:
                self.deposit_money()
            elif choice == 3:
                self.withdraw_money()
            elif choice == 4:
                self.check_balance()
            elif choice == 5:
                self.display_accounts()
            elif choice == 6:
                self.delete_account()
            elif choice == 7:
                self.update_name()
            elif choice == 8:
                self.transfer_money()
            elif choice == 9:
                self.search_accounts()
            elif choice == 10:
                self.transaction_history()
            elif choice == 11:
                print("Thank you for using bank managment system")
                break
            else:
                print("this is not a valid number")
if __name__ == "__main__":
 #   bank = Bank()
   # bank.run()
  start_gui() 