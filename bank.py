from datetime import datetime
class Bank:
    def __init__(self, database):
        self.database = database
        self.transaction_counter = 1000
        conn = self.database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT transaction_id FROM transactions")
            ids = cursor.fetchall()
            for row in ids:
                transaction_id = row[0]
                if transaction_id.startswith("TXN") and not transaction_id.endswith("-R"):
                    number = transaction_id[3:]
                    if number.isdigit():
                        self.transaction_counter = max(
                            self.transaction_counter,
                            int(number)
                        )
        finally:
            conn.close()
    def generate_transaction_id(self):
        self.transaction_counter += 1
        return f"TXN{self.transaction_counter}"
    def get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def generate_account_number(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()
    
        try:
            while True:
                cursor.execute(
                    "SELECT MAX(account_number) FROM accounts"
                )
    
                result = cursor.fetchone()
                last_number = result[0]
    
                if last_number is None:
                    return 7454100001
    
                new_number = last_number + 1
    
                cursor.execute(
                    "SELECT account_number FROM accounts WHERE account_number = ?",
                    (new_number,)
                )
    
                if cursor.fetchone() is None:
                    return new_number
    
        finally:
            conn.close()

    def create_account(self, name, balance=0):
        conn = self.database.get_connection()
        cursor = conn.cursor()
    
        try:
            account_number = self.generate_account_number()
    
            cursor.execute(
                """
                INSERT INTO accounts (account_number, name, balance)
                VALUES (?, ?, ?)
                """,
                (account_number, name, balance)
            )
    
            if balance > 0:
                cursor.execute(
                    """
                    INSERT INTO transactions
                    (transaction_id, account_number, transaction_type,
                     amount, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        self.generate_transaction_id(),
                        account_number,
                        "Initial Deposit",
                        balance,
                        self.get_timestamp()
                    )
                )
    
            conn.commit()
            return account_number
    
        except Exception as e:
            conn.rollback()
            print("Account Creation Error:", e)
            return None
    
        finally:
            conn.close()

    def deposit(self, account_number, amount):
        if amount <= 0:
            return False
        conn = self.database.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT status FROM accounts WHERE account_number = ?",
                (account_number,)
            )
            
            account = cursor.fetchone()
            
            if account is None:
                return False
            
            if account[0] != "Active":
                return False
            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance + ?
                WHERE account_number = ?
                """,
                (amount, account_number)
            )
            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number, transaction_type,
                 amount, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.generate_transaction_id(),
                    account_number,
                    "Deposit",
                    amount,
                    self.get_timestamp()
                )
            )

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("Deposit Error:", e)
            return False

        finally:
            conn.close()

    def withdraw(self, account_number, amount):
        if amount <= 0:
            return False

        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT balance , status FROM accounts WHERE account_number = ?",
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                return False
            if account[1] != "Active":
                return False
            if account[0] < amount:
                return False

            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance - ?
                WHERE account_number = ?
                """,
                (amount, account_number)
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number, transaction_type,
                 amount, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.generate_transaction_id(),
                    account_number,
                    "Withdraw",
                    amount,
                    self.get_timestamp()
                )
            )

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("Withdrawal Error:", e)
            return False

        finally:
            conn.close()
    def delete_account(self, account_number):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT account_number FROM accounts WHERE account_number = ?",
                (account_number,)
            )

            if cursor.fetchone() is None:
                return "not_found"

            cursor.execute(
                """
                SELECT 1 FROM transactions
                WHERE account_number = ? OR receiver_account = ?
                LIMIT 1
                """,
                (account_number, account_number)
            )

            if cursor.fetchone() is not None:
                return "has_transactions"

            cursor.execute(
                "DELETE FROM accounts WHERE account_number = ?",
                (account_number,)
            )

            conn.commit()
            return "deleted"

        except Exception as e:
            conn.rollback()
            print("Delete Account Error:", e)
            return "error"

        finally:
            conn.close()
    
    def check_balance(self, account_number):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = ?",
                (account_number,)
            )

            account = cursor.fetchone()
            return account[0] if account else None

        finally:
            conn.close()

    def transaction_history(self, account_number):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT transaction_id, transaction_type, amount, timestamp
                FROM transactions
                WHERE account_number = ?
                ORDER BY ROWID DESC
                """,
                (account_number,)
            )

            return cursor.fetchall()

        finally:
            conn.close()

    def transfer(self, sender_account, receiver_account, amount):
        if amount <= 0 or sender_account == receiver_account:
            return False

        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT balance, status
                FROM accounts
                WHERE account_number = ?
                """,
                (sender_account,)
            )
            sender = cursor.fetchone()
            
            cursor.execute(
                """
                SELECT status
                FROM accounts
                WHERE account_number = ?
                """,
                (receiver_account,)
            )
            receiver = cursor.fetchone()
            if sender is None or receiver is None:
                return False

            if sender[1] != "Active" or receiver[0] != "Active":
                return False
            if sender[0] < amount:
                return False

            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance - ?
                WHERE account_number = ?
                """,
                (amount, sender_account)
            )

            cursor.execute(
                """
                UPDATE accounts
                SET balance = balance + ?
                WHERE account_number = ?
                """,
                (amount, receiver_account)
            )

            transaction_id = self.generate_transaction_id()
            timestamp = self.get_timestamp()

            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number, transaction_type,
                 amount, timestamp, receiver_account)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction_id,
                    sender_account,
                    "Transfer money",
                    amount,
                    timestamp,
                    receiver_account
                )
            )

            cursor.execute(
                """
                INSERT INTO transactions
                (transaction_id, account_number, transaction_type,
                 amount, timestamp)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    transaction_id + "-R",
                    receiver_account,
                    "Received money",
                    amount,
                    timestamp
                )
            )

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print("Transfer Error:", e)
            return False

        finally:
            conn.close()
    def update_customer_name(self, account_number, new_name):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT account_number FROM accounts WHERE account_number = ?",
                (account_number,)
            )

            if cursor.fetchone() is None:
                return "not_found"

            if not new_name.strip():
                return "invalid_name"

            cursor.execute(
                """
                UPDATE accounts
                SET name = ?
                WHERE account_number = ?
                """,
                (new_name.strip(), account_number)
            )

            conn.commit()
            return "updated"

        except Exception as e:
            conn.rollback()
            print("Update Name Error:", e)
            return "error"

        finally:
            conn.close()
    def get_all_accounts(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT account_number, name, balance
                FROM accounts
                ORDER BY account_number
            """)

            accounts = cursor.fetchall()
            return accounts

        except Exception as e:
            print("Fetch Accounts Error:", e)
            return None

        finally:
            conn.close()
    def search_account(self, account_number):
        conn = self.database.get_connection()
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
            return account

        except Exception as e:
            print("Search Account Error:", e)
            return None

        finally:
            conn.close()
    def get_account_status(self, account_number):

        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT status
                FROM accounts
                WHERE account_number = ?
                """,
                (account_number,)
            )

            result = cursor.fetchone()

            if result is None:
                return None

            return result[0]

        except Exception as e:
            print("Account Status Error:", e)
            return None

        finally:
            conn.close()
            
    def close_account(self, account_number):

        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT status,balance FROM accounts WHERE account_number = ?",
                (account_number,)
            )

            account = cursor.fetchone()

            if account is None:
                return "not_found"

            if account[0] == "Closed":
                return "already_closed"
            if account[1] >0:
                return "balance_remaining"

            cursor.execute(
                """
                UPDATE accounts
                SET status = 'Closed'
                WHERE account_number = ?
                """,
                (account_number,)
            )

            conn.commit()
            return "closed"

        except Exception as e:
            conn.rollback()
            print("Close Account Error:", e)
            return "error"

        finally:
            conn.close()

    def get_account_statement(self, account_number):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT
                    transaction_id,
                    transaction_type,
                    amount,
                    timestamp,
                    receiver_account
                FROM transactions
                WHERE account_number = ?
                ORDER BY ROWID DESC
                """,
                (account_number,)
            )

            return cursor.fetchall()

        except Exception as e:
            print("Account Statement Error:", e)
            return None

        finally:
            conn.close()
    def get_account_summary(self, account_number):
        conn = self.database.get_connection()
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
                return None

            name, balance = account

            cursor.execute(
                """
                SELECT
                    transaction_type,
                    COUNT(*),
                    SUM(amount)
                FROM transactions
                WHERE account_number = ?
                GROUP BY transaction_type
                """,
                (account_number,)
            )

            transactions = cursor.fetchall()

            total_deposits = 0
            total_withdrawals = 0
            total_transactions = 0

            for txn_type, count, amount in transactions:
                total_transactions += count

                if txn_type in ("Deposit", "Received money"):
                    total_deposits += amount

                elif txn_type in ("Withdraw", "Transfer money"):
                    total_withdrawals += amount

            return (
                name,
                balance,
                total_deposits,
                total_withdrawals,
                total_transactions
            )

        except Exception as e:
            print("Account Summary Error:", e)
            return None

        finally:
            conn.close()
    def get_dashboard_stats(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()
    
        try:
            cursor.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(balance), 0),
    
                    SUM(CASE
                        WHEN status = 'Active' THEN 1
                        ELSE 0
                    END),
    
                    SUM(CASE
                        WHEN status = 'Closed' THEN 1
                        ELSE 0
                    END)
    
                FROM accounts
            """)
    
            account_data = cursor.fetchone()
    
            cursor.execute("""
                SELECT COUNT(*)
                FROM transactions
            """)
    
            transaction_count = cursor.fetchone()[0]
    
            cursor.execute("""
                SELECT
                    COALESCE(SUM(
                        CASE
                            WHEN transaction_type IN ('Deposit', 'Received money')
                            THEN amount ELSE 0
                        END
                    ), 0),
    
                    COALESCE(SUM(
                        CASE
                            WHEN transaction_type IN ('Withdraw', 'Transfer money')
                            THEN amount ELSE 0
                        END
                    ), 0)
    
                FROM transactions
            """)
    
            deposit_total, withdrawal_total = cursor.fetchone()
    
            return {
                "total_accounts": account_data[0],
                "total_balance": account_data[1],
                "active_accounts": account_data[2] or 0,
                "closed_accounts": account_data[3] or 0,
                "total_transactions": transaction_count,
                "total_deposits": deposit_total,
                "total_withdrawals": withdrawal_total
            }
    
        except Exception as e:
            print("Dashboard Stats Error:", e)
            return None
    
        finally:
            conn.close()
            
    def get_recent_transactions(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()
    
        try:
            cursor.execute("""
                SELECT
                    t.transaction_id,
                    a.name,
                    t.account_number,
                    t.transaction_type,
                    t.amount,
                    t.timestamp
                FROM transactions t
                JOIN accounts a
                ON t.account_number = a.account_number
                ORDER BY t.ROWID DESC
            """)
    
            return cursor.fetchall()
    
        except Exception as e:
            print("Recent Transactions Error:", e)
            return None
    
        finally:
            conn.close()