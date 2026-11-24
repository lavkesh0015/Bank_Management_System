🏦 Bank Management System (SBMS)

📌 Project Overview
The Bank Management System (SBMS) is a Python-based banking application developed to manage basic banking operations efficiently.
The application uses Python, Tkinter, and SQLite database to provide a user-friendly graphical interface for managing customer accounts and financial transactions.
It allows users to create accounts, deposit money, withdraw money, transfer funds, check account balances, search customer accounts, and view transaction history.

✨ Features
Create new bank accounts
Check account balance
Deposit money
Withdraw money
Transfer money between accounts
Delete bank accounts
Update customer names
Display all registered accounts
Search customer accounts
View transaction history
Generate unique transaction IDs
New receiver warning during money transfers
High-value transaction warning
Transfer confirmation before processing
SQLite database for permanent data storage
User-friendly graphical interface using Tkinter
Search and filter customer accounts

🛠️ Technologies Used
Technology	Purpose
Python	Core programming language
Tkinter	Graphical User Interface
SQLite3	Database management
Datetime	Transaction date and time

📂 Project Structure
text
Bank-Management-System/
│
├── main.py
│
├── bank_management_system/
│   ├── __init__.py
│   ├── bank.py
│   ├── database.py
│   ├── gui.py
│   └── bank_management_system.py
│
├── bank.db
│
├── README.md
│
├── requirements.txt
│
├── .gitignore
│
└── __pycache__/

📁 File Description
main.py – Entry point of the application. Starts the banking system.
bank.py – Contains the Bank class and banking operations.
database.py – Handles SQLite database initialization and management.
gui.py – Contains the graphical user interface.
bank_management_system.py – Contains additional banking system functionality, if used by the application.
init.py – Makes the folder a Python package.
bank.db – SQLite database file used to store accounts and transactions.
README.md – Project documentation.
requirements.txt – Lists project dependencies.
.gitignore – Specifies files and folders Git should ignore.
pycache/ – Automatically generated Python cache files.

Note: Keep only the modules actually used by your application. Avoid duplicate Bank classes or duplicate functionality across Python files.



No external Python packages are required because the project uses Python's standard library.

🚀 Installation and Setup
1. Clone the Repository
bash
git clone <your-repository-link>

2. Open the Project Folder
bash
cd Bank-Management-System

3. Run the Application
bash
python main.py


The Bank Management System graphical interface will open.

🗄️ Database Structure

The application uses SQLite database to store banking information.

It contains two main tables:

1. Accounts Table
Column	Description
account_number	Unique account number
name	Customer name
balance	Current account balance
2. Transactions Table
Column	Description
transaction_id	Unique transaction ID
account_number	Account associated with transaction
transaction_type	Deposit, Withdraw, Transfer money, etc.
amount	Transaction amount
timestamp	Transaction date and time
receiver_account	Receiver account number, if applicable

The database is initialized automatically when the application starts.

💻 Application Modules
Account Management
Create new customer accounts.
Update customer information.
Search customer accounts.
Display all accounts.
Delete existing accounts.
Transaction Management
Deposit money.
Withdraw money.
Transfer money.
Generate transaction IDs.
Maintain transaction records.
Account Information
Check account balance.
View customer profiles.
Generate account statements.
View transaction history.
🔐 Validation and Safety Features
Prevents withdrawals exceeding the available balance.
Validates account numbers and transaction amounts.
Uses parameterized SQL queries.
Provides confirmation before account deletion.
Displays warnings for new receivers.
Displays warnings for high-value transfers.
Uses database rollback when database operations fail.
🔮 Future Improvements
User login and authentication system.
Admin dashboard.
Password protection.
PDF account statement generation.
Enhanced data security and encryption.
Database backup and recovery.
Advanced transaction reports.
👨‍💻 Author

Developed as a Python-based Bank Management System project.

📜 License

This project is created for educational and learning purposes.