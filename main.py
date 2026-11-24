import tkinter as tk

from database import Database
from bank import Bank
from gui import BankGUI


def main():
    db = Database()
    db.create_tables()

    bank = Bank(db)

    root = tk.Tk()

    app = BankGUI(root, bank)

    root.mainloop()


if __name__ == "__main__":
    main() 