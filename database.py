import sqlite3
import hashlib
import secrets
class Database:
    def __init__(self, db_name="bank.db"):
        self.db_name = db_name
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_number INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )
        """)
        cursor.execute("PRAGMA table_info(accounts)")
        columns = [column[1] for column in cursor.fetchall()]

        if "status" not in columns:
            cursor.execute("""
                ALTER TABLE accounts
                ADD COLUMN status TEXT NOT NULL DEFAULT 'Active'
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)
        cursor.execute("PRAGMA table_info(admins)")
        admin_columns = [
            column[1] for column in cursor.fetchall()
        ]

        if "recovery_hash" not in admin_columns:
            cursor.execute("""
                ALTER TABLE admins
                ADD COLUMN recovery_hash TEXT
            """)

        if "recovery_salt" not in admin_columns:
            cursor.execute("""
                ALTER TABLE admins
                ADD COLUMN recovery_salt TEXT
            """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    def log_activity(self, username, action, details=""):

        from datetime import datetime

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute("""
                INSERT INTO activity_logs
                (username, action, details, timestamp)
                VALUES (?, ?, ?, ?)
            """, (
                username,
                action,
                details,
                timestamp
            ))

            conn.commit()
            return True

        except Exception as e:
            print("Activity Log Error:", e)
            conn.rollback()
            return False

        finally:
            conn.close()
    def get_activity_logs(self):

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    log_id,
                    username,
                    action,
                    details,
                    timestamp
                FROM activity_logs
                ORDER BY log_id DESC
            """)

            logs = cursor.fetchall()
            return logs

        except Exception as e:
            print("Get Activity Logs Error:", e)
            return []

        finally:
            conn.close()
    def search_activity_logs(self, search_text="", action="All"):

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT
                    log_id,
                    username,
                    action,
                    details,
                    timestamp
                FROM activity_logs
                WHERE (
                    username LIKE ?
                    OR action LIKE ?
                    OR details LIKE ?
                )
            """

            search_value = f"%{search_text}%"
            params = [
                search_value,
                search_value,
                search_value
            ]

            if action != "All":
                query += " AND action = ?"
                params.append(action)

            query += " ORDER BY log_id DESC"

            cursor.execute(query, params)

            return cursor.fetchall()

        except Exception as e:
            print("Search Activity Logs Error:", e)
            return []

        finally:
            conn.close()
    def create_admin(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            salt = secrets.token_bytes(16)

            password_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                200000
            )

            cursor.execute(
                """
                INSERT INTO admins (username, password_hash, salt)
                VALUES (?, ?, ?)
                """,
                (username, password_hash.hex(), salt.hex())
            )

            conn.commit()
            return "created"

        except sqlite3.IntegrityError:
            return "username_exists"

        except Exception as e:
            print("Create Admin Error:", e)
            return "error"

        finally:
            conn.close()
    def verify_admin(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT password_hash, salt
                FROM admins
                WHERE username = ?
                """,
                (username,)
            )

            admin = cursor.fetchone()

            if admin is None:
                return False

            stored_hash, stored_salt = admin

            salt = bytes.fromhex(stored_salt)

            entered_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                200000
            )

            return secrets.compare_digest(
                entered_hash.hex(),
                stored_hash
            )

        except Exception as e:
            print("Verify Admin Error:", e)
            return False

        finally:
            conn.close()
    def generate_recovery_code(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT recovery_hash
                FROM admins
                WHERE username = ?
                """,
                (username,)
            )

            admin = cursor.fetchone()

            if admin is None:
                return None

            if admin[0] is not None:
                return "already_exists"

            recovery_code = secrets.token_hex(8)
            salt = secrets.token_bytes(16)

            recovery_hash = hashlib.pbkdf2_hmac(
                "sha256",
                recovery_code.encode("utf-8"),
                salt,
                200000
            )

            cursor.execute(
                """
                UPDATE admins
                SET recovery_hash = ?, recovery_salt = ?
                WHERE username = ?
                """,
                (recovery_hash.hex(), salt.hex(), username)
            )

            conn.commit()
            return recovery_code

        except Exception as e:
            print("Recovery Code Error:", e)
            return None

        finally:
            conn.close()
    def has_recovery_code(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT recovery_hash
                FROM admins
                WHERE username = ?
                """,
                (username,)
            )

            result = cursor.fetchone()

            return result is not None and result[0] is not None

        except Exception as e:
            print("Check Recovery Code Error:", e)
            return False

        finally:
            conn.close()

    def verify_recovery_code(self, username, recovery_code):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT recovery_hash, recovery_salt
                FROM admins
                WHERE username = ?
                """,
                (username,)
            )

            admin = cursor.fetchone()

            if admin is None or not admin[0] or not admin[1]:
                return False

            stored_hash, stored_salt = admin

            salt = bytes.fromhex(stored_salt)

            entered_hash = hashlib.pbkdf2_hmac(
                "sha256",
                recovery_code.encode("utf-8"),
                salt,
                200000
            )

            return secrets.compare_digest(
                entered_hash.hex(),
                stored_hash
            )

        except Exception as e:
            print("Recovery Verification Error:", e)
            return False

        finally:
            conn.close()
    def reset_admin_password(self, username, recovery_code, new_password):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT recovery_hash, recovery_salt
                FROM admins
                WHERE username = ?
                """,
                (username,)
            )

            admin = cursor.fetchone()

            if admin is None or not admin[0] or not admin[1]:
                return "invalid_recovery"

            stored_hash, stored_salt = admin

            salt = bytes.fromhex(stored_salt)

            entered_hash = hashlib.pbkdf2_hmac(
                "sha256",
                recovery_code.encode("utf-8"),
                salt,
                200000
            )

            if not secrets.compare_digest(
                entered_hash.hex(),
                stored_hash
            ):
                return "invalid_recovery"

            new_salt = secrets.token_bytes(16)

            new_hash = hashlib.pbkdf2_hmac(
                "sha256",
                new_password.encode("utf-8"),
                new_salt,
                200000
            )

            cursor.execute(
                """
                UPDATE admins
                SET password_hash = ?,
                    salt = ?,
                    recovery_hash = NULL,
                    recovery_salt = NULL
                WHERE username = ?
                """,
                (new_hash.hex(), new_salt.hex(), username)
            )

            conn.commit()
            return "updated"

        except Exception as e:
            print("Password Reset Error:", e)
            conn.rollback()
            return "error"

        finally:
            conn.close()
    def change_admin_password(self, username, current_password, new_password):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT password_hash, salt
                FROM admins
                WHERE username = ?
                """,
                (username,)
            )

            admin = cursor.fetchone()

            if admin is None:
                return "not_found"

            stored_hash, stored_salt = admin

            current_hash = hashlib.pbkdf2_hmac(
                "sha256",
                current_password.encode("utf-8"),
                bytes.fromhex(stored_salt),
                200000
            )

            if not secrets.compare_digest(
                current_hash.hex(),
                stored_hash
            ):
                return "invalid_password"

            new_salt = secrets.token_bytes(16)

            new_hash = hashlib.pbkdf2_hmac(
                "sha256",
                new_password.encode("utf-8"),
                new_salt,
                200000
            )

            cursor.execute(
                """
                UPDATE admins
                SET password_hash = ?, salt = ?
                WHERE username = ?
                """,
                (new_hash.hex(), new_salt.hex(), username)
            )

            conn.commit()
            return "updated"

        except Exception as e:
            print("Change Password Error:", e)
            conn.rollback()
            return "error"

        finally:
            conn.close()

    def has_admins(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM admins")
            count = cursor.fetchone()[0]
            return count > 0

        except Exception as e:
            print("Admin Check Error:", e)
            return False

        finally:
            conn.close()