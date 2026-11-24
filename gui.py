import tkinter as tk
from tkinter import messagebox, simpledialog,ttk
class BankGUI:

    def __init__(self, root, bank):
        self.root = root
        self.bank = bank

        self.root.title("Bank Management System")
        self.root.geometry("900x650")
        self.root.configure(bg="#eaf0f6")

        self.show_login_screen()
    def show_login_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("850x560")
        self.root.configure(bg="#eaf0f6")
        self.root.resizable(True, True)

        is_first_admin = not self.bank.database.has_admins()

        title_text = (
            "Create Admin Account"
            if is_first_admin else "Welcome Back"
        )

        # Main Container
        main_frame = tk.Frame(
            self.root,
            bg="white"
        )
        main_frame.pack(
            expand=True,
            fill="both",
            padx=25,
            pady=25
        )

        # LEFT BRANDING PANEL
        left_frame = tk.Frame(
            main_frame,
            bg="#102746",
            width=300
        )
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)

        logo_canvas = tk.Canvas(
            left_frame,
            width=120,
            height=100,
            bg="#102746",
            highlightthickness=0
        )
        logo_canvas.pack(pady=(75, 15))

        logo_canvas.create_polygon(
            60, 10, 15, 35, 105, 35,
            fill="#38bdf8",
            outline="#38bdf8"
        )

        logo_canvas.create_rectangle(
            20, 38, 100, 45,
            fill="#38bdf8",
            outline="#38bdf8"
        )

        for x in [30, 48, 66, 84]:
            logo_canvas.create_rectangle(
                x, 46, x + 8, 82,
                fill="white",
                outline="white"
            )

        logo_canvas.create_rectangle(
            15, 83, 105, 90,
            fill="#38bdf8",
            outline="#38bdf8"
        )

        tk.Label(
            left_frame,
            text="SECURE BANKING",
            font=("Arial", 19, "bold"),
            bg="#102746",
            fg="white"
        ).pack(pady=5)

        tk.Label(
            left_frame,
            text="Bank Management System",
            font=("Arial", 10),
            bg="#102746",
            fg="#cbd5e1"
        ).pack()

        tk.Label(
            left_frame,
            text="SAFE  •  SECURE  •  RELIABLE",
            font=("Arial", 9, "bold"),
            bg="#102746",
            fg="#38bdf8"
        ).pack(pady=35)

        tk.Label(
            left_frame,
            text="Administrator Access",
            font=("Arial", 10),
            bg="#102746",
            fg="#94a3b8"
        ).pack(side="bottom", pady=25)

        # RIGHT LOGIN PANEL
        right_frame = tk.Frame(
            main_frame,
            bg="white",
            padx=45,
            pady=35
        )
        right_frame.pack(
            side="left",
            expand=True,
            fill="both"
        )

        tk.Label(
            right_frame,
            text="BANK MANAGEMENT SYSTEM",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#2563eb"
        ).pack(pady=(15, 12))

        tk.Label(
            right_frame,
            text=title_text,
            font=("Arial", 25, "bold"),
            bg="white",
            fg="#102746"
        ).pack()

        tk.Label(
            right_frame,
            text=(
                "Create your administrator account"
                if is_first_admin
                else "Sign in to your administrator account"
            ),
            font=("Arial", 10),
            bg="white",
            fg="#64748b"
        ).pack(pady=(8, 30))

        # Username
        tk.Label(
            right_frame,
            text="Username",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#334155"
        ).pack(anchor="w")

        username_entry = tk.Entry(
            right_frame,
            font=("Arial", 12),
            bd=1,
            relief="solid"
        )
        username_entry.pack(fill="x", ipady=9, pady=(7, 18))

        # Password
        tk.Label(
            right_frame,
            text="Password",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#334155"
        ).pack(anchor="w")

        password_frame = tk.Frame(
            right_frame,
            bg="white",
            bd=1,
            relief="solid"
        )
        password_frame.pack(
            fill="x",
            pady=(7, 20)
        )

        password_entry = tk.Entry(
            password_frame,
            font=("Arial", 12),
            show="*",
            bd=0,
            relief="flat"
        )
        password_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10,
            padx=8
        )

        def toggle_password():

            if password_entry.cget("show") == "*":
                password_entry.config(show="")
                eye_button.config(text="Hide")
            else:
                password_entry.config(show="*")
                eye_button.config(text="Show")

        eye_button = tk.Button(
            password_frame,
            text="Show",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#2563eb",
            bd=0,
            cursor="hand2",
            command=toggle_password
        )
        eye_button.pack(side="right", padx=10)

        # LOGIN / CREATE ADMIN LOGIC
        def submit_login():

            username = username_entry.get().strip()
            password = password_entry.get()

            if not username or not password:
                messagebox.showwarning(
                    "Missing Details",
                    "Please enter username and password.",
                    parent=self.root
                )
                return

            if is_first_admin:

                if len(password) < 8:
                    messagebox.showwarning(
                        "Weak Password",
                        "Password must contain at least 8 characters.",
                        parent=self.root
                    )
                    return

                result = self.bank.database.create_admin(
                    username,
                    password
                )

                if result == "created":
                    messagebox.showinfo(
                        "Success",
                        "Admin account created successfully.",
                        parent=self.root
                    )
                    self.show_login_screen()

                elif result == "username_exists":
                    messagebox.showerror(
                        "Error",
                        "Username already exists.",
                        parent=self.root
                    )

                else:
                    messagebox.showerror(
                        "Error",
                        "Unable to create admin account.",
                        parent=self.root
                    )

            else:

                valid = self.bank.database.verify_admin(
                    username,
                    password
                )

                if valid:
                    self.admin_username = username
                    self.bank.database.log_activity(
                        username,
                        "Login",
                        "Admin logged in successfully "
                    )

                    for widget in self.root.winfo_children():
                        widget.destroy()

                    self.create_widgets()

                else:
                    messagebox.showerror(
                        "Login Failed",
                        "Invalid username or password.",
                        parent=self.root
                    )

        # SIGN IN BUTTON
        tk.Button(
            right_frame,
            text="CREATE ADMIN ACCOUNT" if is_first_admin else "SIGN IN",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            command=submit_login,
            pady=12
        ).pack(fill="x", pady=(5, 12))

        # FORGOT PASSWORD
        if not is_first_admin:

            tk.Button(
                right_frame,
                text="Forgot Password?",
                font=("Arial", 10, "underline"),
                bg="white",
                fg="#2563eb",
                activebackground="white",
                activeforeground="#1d4ed8",
                bd=0,
                cursor="hand2",
                command=self.forgot_password
            ).pack(pady=5)

        tk.Label(
            right_frame,
            text="🔒 Secure Administrator Access",
            font=("Arial", 9),
            bg="white",
            fg="#64748b"
        ).pack(side="bottom", pady=5)

    def logout(self):

        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self.root
        )

        if confirm:
            self.bank.database.log_activity(
                self.admin_username,
                "Logout",
                "Admin logged out successfully"
            )
            self.show_login_screen()
    def admin_activity_log(self):

        window = tk.Toplevel(self.root)
        window.title("Admin Activity Log")
        window.geometry("1100x650")
        window.configure(bg="#f1f5f9")
        window.minsize(850, 500)

        # Main Container
        main_frame = tk.Frame(
            window,
            bg="#f1f5f9",
            padx=25,
            pady=20
        )
        main_frame.pack(fill="both", expand=True)

        # Header
        header = tk.Frame(
            main_frame,
            bg="#102746",
            padx=22,
            pady=20
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="ADMIN ACTIVITY LOG",
            font=("Arial", 20, "bold"),
            bg="#102746",
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Monitor administrator activities and account operations",
            font=("Arial", 10),
            bg="#102746",
            fg="#cbd5e1"
        ).pack(anchor="w", pady=(5, 0))

        # Search and Filter
        search_frame = tk.Frame(
            main_frame,
            bg="white",
            padx=15,
            pady=15
        )
        search_frame.pack(fill="x", pady=18)

        tk.Label(
            search_frame,
            text="Search:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(side="left", padx=(0, 8))

        search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            width=25,
            relief="solid",
            bd=1
        )
        search_entry.pack(side="left", padx=5, ipady=6)

        tk.Label(
            search_frame,
            text="Action:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(side="left", padx=(15, 5))

        filter_combo = ttk.Combobox(
            search_frame,
            values=[
                "All",
                "Login",
                "Logout",
                "Create Account",
                "Deposit",
                "Withdraw",
                "Transfer",
                "Close Account",
                "Delete Account",
                "Update Customer Name",
                "Change Password",
                "Reset Password"
            ],
            state="readonly",
            width=22,
            font=("Arial", 10)
        )
        filter_combo.set("All")
        filter_combo.pack(side="left", padx=5, ipady=4)

        # Table Container
        table_frame = tk.Frame(
            main_frame,
            bg="white",
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True)

        columns = (
            "Log ID",
            "Admin Username",
            "Action",
            "Details",
            "Date & Time"
        )

        style = ttk.Style()
        style.configure(
            "Activity.Treeview",
            background="white",
            foreground="#142d4e",
            rowheight=35,
            font=("Arial", 10),
            fieldbackground="white"
        )

        style.configure(
            "Activity.Treeview.Heading",
            background="#24577a",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=10
        )

        style.map(
            "Activity.Treeview",
            background=[("selected", "#3478b8")],
            foreground=[("selected", "white")]
        )

        activity_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Activity.Treeview"
        )

        widths = {
            "Log ID": 70,
            "Admin Username": 150,
            "Action": 180,
            "Details": 400,
            "Date & Time": 180
        }

        for column in columns:
            activity_table.heading(
                column,
                text=column
            )

            activity_table.column(
                column,
                width=widths[column],
                minwidth=70,
                anchor="center"
            )

        activity_table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=activity_table.yview
        )
        vertical_scrollbar.pack(side="right", fill="y")

        horizontal_scrollbar = ttk.Scrollbar(
            main_frame,
            orient="horizontal",
            command=activity_table.xview
        )
        horizontal_scrollbar.pack(fill="x")

        activity_table.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        # Load Activity Logs
        def load_logs():

            activity_table.delete(
                *activity_table.get_children()
            )

            logs = self.bank.database.search_activity_logs(
                search_entry.get().strip(),
                filter_combo.get()
            )

            for log in logs:
                activity_table.insert(
                    "",
                    "end",
                    values=log
                )

        # Buttons
        button_frame = tk.Frame(
            main_frame,
            bg="#f1f5f9"
        )
        button_frame.pack(fill="x", pady=15)

        tk.Button(
            button_frame,
            text="SEARCH",
            command=load_logs,
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="REFRESH",
            command=load_logs,
            font=("Arial", 10, "bold"),
            bg="#24577a",
            fg="white",
            activebackground="#163d59",
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=10
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="CLOSE",
            command=window.destroy,
            font=("Arial", 10, "bold"),
            bg="#64748b",
            fg="white",
            activebackground="#475569",
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=10
        ).pack(side="right", padx=5)

        load_logs()  
    def forgot_password(self):

        window = tk.Toplevel(self.root)
        window.title("Reset Admin Password")
        window.geometry("520x700")
        window.configure(bg="#eaf0f6")
        window.resizable(False, False)
    
        # Main Card
        main_frame = tk.Frame(
            window,
            bg="white",
            bd=0
        )
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )
    
        # Navy Header
        header = tk.Frame(
            main_frame,
            bg="#102746",
            height=145
        )
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="🔐",
            font=("Arial", 30),
            bg="#102746",
            fg="white"
        ).pack(pady=(18, 2))
    
        tk.Label(
            header,
            text="PASSWORD RECOVERY",
            font=("Arial", 17, "bold"),
            bg="#102746",
            fg="white"
        ).pack()
    
        tk.Label(
            header,
            text="Secure your administrator account",
            font=("Arial", 9),
            bg="#102746",
            fg="#cbd5e1"
        ).pack(pady=5)
    
        # Form Area
        form = tk.Frame(
            main_frame,
            bg="white",
            padx=35,
            pady=22
        )
        form.pack(fill="both", expand=True)
    
        tk.Label(
            form,
            text="Reset Your Password",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(anchor="w")
    
        tk.Label(
            form,
            text="Enter your account details and recovery code.",
            font=("Arial", 9),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w", pady=(4, 18))
    
        def create_field(label_text, show=None):
    
            tk.Label(
                form,
                text=label_text,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#334155"
            ).pack(anchor="w", pady=(8, 5))
    
            field_frame = tk.Frame(
                form,
                bg="#f8fafc",
                highlightbackground="#cbd5e1",
                highlightthickness=1
            )
            field_frame.pack(fill="x")
    
            entry = tk.Entry(
                field_frame,
                font=("Arial", 11),
                bg="#f8fafc",
                fg="#142d4e",
                bd=0,
                show=show
            )
            entry.pack(
                fill="x",
                padx=12,
                pady=10
            )
    
            return entry
    
        username_entry = create_field("Username")
        recovery_entry = create_field("Recovery Code")
        new_entry = create_field("New Password", show="*")
        confirm_entry = create_field("Confirm New Password", show="*")
    
        def reset_password():
    
            username = username_entry.get().strip()
            recovery_code = recovery_entry.get().strip()
            new_password = new_entry.get()
            confirm_password = confirm_entry.get()
    
            if not username or not recovery_code or not new_password or not confirm_password:
                messagebox.showwarning(
                    "Missing Details",
                    "Please fill all fields.",
                    parent=window
                )
                return
    
            if len(new_password) < 8:
                messagebox.showwarning(
                    "Weak Password",
                    "New password must contain at least 8 characters.",
                    parent=window
                )
                return
    
            if new_password != confirm_password:
                messagebox.showerror(
                    "Password Mismatch",
                    "New passwords do not match.",
                    parent=window
                )
                return
    
            result = self.bank.database.reset_admin_password(
                username,
                recovery_code,
                new_password
            )
    
            if result == "updated":
                # Save Password Reset Activity
                self.bank.database.log_activity(
                    username,
                    "Reset Password",
                    "Admin password reset successfully using recovery code"
                )
                messagebox.showinfo(
         
                    "Success",
                    "Password reset successfully. Please login again.",
                    parent=window
                )
                window.destroy()
    
            elif result == "invalid_recovery":
                messagebox.showerror(
                    "Invalid Recovery Code",
                    "Username or recovery code is incorrect.",
                    parent=window
                )
    
            else:
                messagebox.showerror(
                    "Error",
                    "Unable to reset password.",
                    parent=window
                )
    
        # Reset Button
        tk.Button(
            form,
            text="RESET PASSWORD",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            cursor="hand2",
            command=reset_password,
            bd=0,
            pady=12
        ).pack(fill="x", pady=(22, 8))
    
        tk.Label(
            form,
            text="🔒  Your recovery details are securely verified.",
            font=("Arial", 8),
            bg="white",
            fg="#64748b"
        ).pack(pady=5)
        
    def generate_admin_recovery_code(self):

        username = self.admin_username
    
        if self.bank.database.has_recovery_code(username):

            info_window = tk.Toplevel(self.root)
            info_window.title("Recovery Code Exists")
            info_window.geometry("440x320")
            info_window.configure(bg="#eaf0f6")
            info_window.resizable(False, False)
            info_window.update_idletasks()

            parent_x = self.root.winfo_rootx()
            parent_y = self.root.winfo_rooty()
        
            parent_width = self.root.winfo_width()
            parent_height = self.root.winfo_height()
        
            popup_width = info_window.winfo_width()
            popup_height = info_window.winfo_height()
        
            x = parent_x + (parent_width - popup_width) // 2
            y = parent_y + (parent_height - popup_height) // 2
        
            info_window.geometry(
                f"+{x}+{y}"
            )
            info_window.transient(self.root)
            info_window.grab_set()
        
            card = tk.Frame(info_window, bg="white")
            card.pack(fill="both", expand=True, padx=20, pady=20)
        
            header = tk.Frame(
                card,
                bg="#102746",
                height=105
            )
            header.pack(fill="x")
            header.pack_propagate(False)
        
            tk.Label(
                header,
                text="🔐",
                font=("Arial", 28),
                bg="#102746",
                fg="white"
            ).pack(pady=(10, 0))
        
            tk.Label(
                header,
                text="RECOVERY CODE EXISTS",
                font=("Arial", 14, "bold"),
                bg="#102746",
                fg="white"
            ).pack()
        
            body = tk.Frame(
                card,
                bg="white",
                padx=20,
                pady=20
            )
            body.pack(fill="both", expand=True)
        
            tk.Label(
                body,
                text="Your recovery code is already generated.",
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#142d4e"
            ).pack(pady=(5, 8))
        
            tk.Label(
                body,
                text="Please use your previously saved recovery code.",
                font=("Arial", 9),
                bg="white",
                fg="#64748b",
                wraplength=330
            ).pack(pady=5)
        
            tk.Button(
                body,
                text="OK, GOT IT",
                font=("Arial", 10, "bold"),
                bg="#2563eb",
                fg="white",
                cursor="hand2",
                bd=0,
                pady=10,
                command=info_window.destroy
            ).pack(fill="x", pady=(15, 0))
            return
    
        # Premium Confirmation Window
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Generate Recovery Code")
        confirm_window.geometry("480x380")
        confirm_window.configure(bg="#eaf0f6")
        confirm_window.resizable(False, False)
        confirm_window.transient(self.root)
        confirm_window.grab_set()
    
        card = tk.Frame(confirm_window, bg="white")
        card.pack(fill="both", expand=True, padx=20, pady=20)
    
        header = tk.Frame(
            card,
            bg="#102746",
            height=110
        )
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="🔐",
            font=("Arial", 27),
            bg="#102746",
            fg="white"
        ).pack(pady=(10, 0))
    
        tk.Label(
            header,
            text="RECOVERY CODE",
            font=("Arial", 16, "bold"),
            bg="#102746",
            fg="white"
        ).pack()
    
        body = tk.Frame(
            card,
            bg="white",
            padx=25,
            pady=20
        )
        body.pack(fill="both", expand=True)
    
        tk.Label(
            body,
            text="Generate New Recovery Code?",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(pady=(0, 10))
    
        tk.Label(
            body,
            text=(
                "A recovery code will be generated and shown only once.\n\n"
                "Please save it somewhere secure.\n"
                "You cannot view it again after closing this window."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#64748b",
            justify="center"
        ).pack(pady=5)
    
        def cancel_generation():
            confirm_window.destroy()
    
        def generate_code():
    
            confirm_window.destroy()
    
            recovery_code = self.bank.database.generate_recovery_code(
                username
            )
    
            if recovery_code == "already_exists":
                messagebox.showinfo(
                    "Recovery Code Exists",
                    "A recovery code has already been generated.",
                    parent=self.root
                )
    
            elif recovery_code:
    
                # One-time Recovery Code Window
                result_window = tk.Toplevel(self.root)
                result_window.title("Your Recovery Code")
                result_window.geometry("480x410")
                result_window.configure(bg="#eaf0f6")
                result_window.resizable(False, False)
                result_window.transient(self.root)
                result_window.grab_set()
    
                result_card = tk.Frame(
                    result_window,
                    bg="white"
                )
                result_card.pack(
                    fill="both",
                    expand=True,
                    padx=20,
                    pady=20
                )
    
                result_header = tk.Frame(
                    result_card,
                    bg="#102746",
                    height=115
                )
                result_header.pack(fill="x")
                result_header.pack_propagate(False)
    
                tk.Label(
                    result_header,
                    text="✓",
                    font=("Arial", 30, "bold"),
                    bg="#102746",
                    fg="#38bdf8"
                ).pack(pady=(10, 0))
    
                tk.Label(
                    result_header,
                    text="RECOVERY CODE GENERATED",
                    font=("Arial", 14, "bold"),
                    bg="#102746",
                    fg="white"
                ).pack()
    
                result_body = tk.Frame(
                    result_card,
                    bg="white",
                    padx=25,
                    pady=20
                )
                result_body.pack(fill="both", expand=True)
    
                tk.Label(
                    result_body,
                    text="Your Username",
                    font=("Arial", 9, "bold"),
                    bg="white",
                    fg="#64748b"
                ).pack()
    
                tk.Label(
                    result_body,
                    text=username,
                    font=("Arial", 12, "bold"),
                    bg="white",
                    fg="#142d4e"
                ).pack(pady=(3, 15))
    
                tk.Label(
                    result_body,
                    text="YOUR ONE-TIME RECOVERY CODE",
                    font=("Arial", 9, "bold"),
                    bg="white",
                    fg="#64748b"
                ).pack()
    
                code_entry = tk.Entry(
                    result_body,
                    font=("Arial", 16, "bold"),
                    justify="center",
                    bg="#f1f5f9",
                    fg="#142d4e",
                    bd=1,
                    relief="solid"
                )
                code_entry.pack(fill="x", pady=8, ipady=8)
                code_entry.insert(0, recovery_code)
                code_entry.config(state="readonly")
    
                tk.Label(
                    result_body,
                    text="Save this code securely. It will not be shown again.",
                    font=("Arial", 9, "bold"),
                    bg="white",
                    fg="#dc2626",
                    wraplength=350
                ).pack(pady=(5, 12))
    
                tk.Button(
                    result_body,
                    text="DONE",
                    font=("Arial", 10, "bold"),
                    bg="#2563eb",
                    fg="white",
                    activebackground="#1d4ed8",
                    activeforeground="white",
                    cursor="hand2",
                    bd=0,
                    pady=10,
                    command=result_window.destroy
                ).pack(fill="x")
    
            else:
                messagebox.showerror(
                    "Error",
                    "Unable to generate recovery code.",
                    parent=self.root
                )
    
        # Buttons
        button_frame = tk.Frame(body, bg="white")
        button_frame.pack(fill="x", pady=(15, 0))
    
        tk.Button(
            button_frame,
            text="CANCEL",
            font=("Arial", 10, "bold"),
            bg="#e2e8f0",
            fg="#334155",
            cursor="hand2",
            bd=0,
            pady=10,
            command=cancel_generation
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))
    
        tk.Button(
            button_frame,
            text="GENERATE CODE",
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            cursor="hand2",
            bd=0,
            pady=10,
            command=generate_code
        ).pack(side="left", fill="x", expand=True, padx=(6, 0))
        
    def change_password(self):

        window = tk.Toplevel(self.root)
        window.title("Change Admin Password")
        window.geometry("520x650")
        window.configure(bg="#eaf0f6")
        window.resizable(False, False)
    
        main_frame = tk.Frame(window, bg="white")
        main_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )
    
        # Navy Header
        header = tk.Frame(
            main_frame,
            bg="#102746",
            height=140
        )
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="🔐",
            font=("Arial", 30),
            bg="#102746",
            fg="white"
        ).pack(pady=(15, 2))
    
        tk.Label(
            header,
            text="CHANGE PASSWORD",
            font=("Arial", 17, "bold"),
            bg="#102746",
            fg="white"
        ).pack()
    
        tk.Label(
            header,
            text="Keep your administrator account secure",
            font=("Arial", 9),
            bg="#102746",
            fg="#cbd5e1"
        ).pack(pady=5)
    
        # Form
        form = tk.Frame(
            main_frame,
            bg="white",
            padx=35,
            pady=22
        )
        form.pack(fill="both", expand=True)
    
        tk.Label(
            form,
            text="Update Your Password",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(anchor="w")
    
        tk.Label(
            form,
            text="Enter your current password and choose a new one.",
            font=("Arial", 9),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w", pady=(4, 12))
    
        def create_field(label_text):
    
            tk.Label(
                form,
                text=label_text,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#334155"
            ).pack(anchor="w", pady=(9, 5))
    
            field_frame = tk.Frame(
                form,
                bg="#f8fafc",
                highlightbackground="#cbd5e1",
                highlightthickness=1
            )
            field_frame.pack(fill="x")
    
            entry = tk.Entry(
                field_frame,
                font=("Arial", 11),
                bg="#f8fafc",
                fg="#142d4e",
                bd=0,
                show="*"
            )
            entry.pack(
                fill="x",
                padx=12,
                pady=10
            )
    
            return entry
    
        current_entry = create_field("Current Password")
        new_entry = create_field("New Password")
        confirm_entry = create_field("Confirm New Password")
    
        def update_password():
    
            current = current_entry.get()
            new = new_entry.get()
            confirm = confirm_entry.get()
    
            if not current or not new or not confirm:
                messagebox.showwarning(
                    "Missing Details",
                    "Please fill all fields.",
                    parent=window
                )
                return
    
            if len(new) < 8:
                messagebox.showwarning(
                    "Weak Password",
                    "New password must contain at least 8 characters.",
                    parent=window
                )
                return
    
            if new != confirm:
                messagebox.showerror(
                    "Password Mismatch",
                    "New passwords do not match.",
                    parent=window
                )
                return
    
            if current == new:
                messagebox.showwarning(
                    "Invalid Password",
                    "New password must be different.",
                    parent=window
                )
                return
    
            result = self.bank.database.change_admin_password(
                self.admin_username,
                current,
                new
            )
    
            if result == "updated":
                # Save Password Change Activity
                self.bank.database.log_activity(
                    self.admin_username,
                    "Change Password",
                    "Admin password changed successfully"
                )
                messagebox.showinfo(
                    "Success",
                    "Admin password changed successfully.",
                    parent=window
                )
                window.destroy()
    
            elif result == "invalid_password":
                messagebox.showerror(
                    "Incorrect Password",
                    "Current password is incorrect.",
                    parent=window
                )
    
            else:
                messagebox.showerror(
                    "Error",
                    "Unable to change password.",
                    parent=window
                )
    
        # Update Button
        tk.Button(
            form,
            text="UPDATE PASSWORD",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            cursor="hand2",
            command=update_password,
            bd=0,
            pady=12
        ).pack(fill="x", pady=(22, 8))
        tk.Button(
        form,
        text="CANCEL",
        font=("Arial", 10, "bold"),
        bg="#e2e8f0",
        fg="#334155",
        activebackground="#cbd5e1",
        activeforeground="#142d4e",
        cursor="hand2",
        command=window.destroy,
        bd=0,
        pady=11
    ).pack(fill="x", pady=(5, 8))
    
        tk.Label(
            form,
            text="🔒  Password verification is required.",
            font=("Arial", 8),
            bg="white",
            fg="#64748b"
        ).pack(pady=5)
    
    def create_widgets(self):

        self.root.geometry("900x650")
        self.root.configure(bg="#eaf0f6")
        self.root.title("SBMS - Smart Bank Management System")
        self.root.geometry("1150x750")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#f1f5f9")

        # Main layout
        # Scrollable Sidebar
        sidebar_container = tk.Frame(
            self.root,
            bg="#142d4e",
            width=250
        )
        sidebar_container.pack(side="left", fill="y")
        sidebar_container.pack_propagate(False)

        sidebar_canvas = tk.Canvas(
            sidebar_container,
            bg="#142d4e",
            highlightthickness=0,
            width=230
        )
        sidebar_canvas.pack(side="left", fill="both", expand=True)

        sidebar_scrollbar = ttk.Scrollbar(
            sidebar_container,
            orient="vertical",
            command=sidebar_canvas.yview
        )
        sidebar_scrollbar.pack(side="right", fill="y")

        sidebar_canvas.configure(
            yscrollcommand=sidebar_scrollbar.set
        )

        sidebar = tk.Frame(
            sidebar_canvas,
            bg="#142d4e"
        )

        sidebar_window = sidebar_canvas.create_window(
            (0, 0),
            window=sidebar,
            anchor="nw"
        )

        sidebar.bind(
            "<Configure>",
            lambda event: sidebar_canvas.configure(
                scrollregion=sidebar_canvas.bbox("all")
            )
        )

        sidebar_canvas.bind(
            "<Configure>",
            lambda event: sidebar_canvas.itemconfigure(
                sidebar_window,
                width=event.width
            )
        )

        content = tk.Frame(
            self.root,
            bg="#f1f5f9"
        )
        content.pack(side="left", fill="both", expand=True)

        # Sidebar branding
        tk.Label(
            sidebar,
            text="SBMS",
            font=("Arial", 27, "bold"),
            bg="#142d4e",
            fg="white"
        ).pack(pady=(30, 3))

        tk.Label(
            sidebar,
            text="SMART BANKING SYSTEM",
            font=("Arial", 9, "bold"),
            bg="#142d4e",
            fg="#9bb5d1"
        ).pack(pady=(0, 30))

        tk.Frame(
            sidebar,
            bg="#355273",
            height=1
        ).pack(fill="x", padx=18, pady=5)

        tk.Label(
            sidebar,
            text="MAIN MENU",
            font=("Arial", 9, "bold"),
            bg="#142d4e",
            fg="#9bb5d1",
            anchor="w"
        ).pack(fill="x", padx=22, pady=12)

        # Navigation buttons
        buttons = [
            ("Dashboard", None),
            ("Create Account", self.create_account),
            ("Check Balance", self.check_balance),
            ("Deposit Money", self.deposit),
            ("Withdraw Money", self.withdraw),
            ("Transfer Money", self.transfer_money),
            ("Search Account", self.search_account),
            ("Update Customer Name", self.update_customer_name),
            ("Display All Accounts", self.display_all_accounts),
            ("Transaction History", self.transaction_history),
            ("Account Statement", self.account_statement),
            ("Close Account",self.close_account),
            ("Delete Account", self.delete_account),
            ("Change Password",self.change_password),
            ("Generate Recovery Code",self.generate_admin_recovery_code),
            ("Admin Activity Log",self.admin_activity_log)
        ]

        for text, command in buttons:

            is_dashboard = command is None

            btn = tk.Button(
                sidebar,
                text="  " + text,
                font=("Arial", 10, "bold"),
                bg="#24476b" if is_dashboard else "#142d4e",
                fg="white",
                activebackground="#315b83",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=15,
                pady=10,
                cursor="hand2",
                command=command if command else lambda: None
            )
            btn.pack(fill="x", padx=12, pady=2)
        # Logout Button
        tk.Frame(
            sidebar,
            bg="#355273",
            height=1
        ).pack(fill="x", padx=18, pady=15)

        tk.Button(
            sidebar,
            text="  Logout",
            font=("Arial", 10, "bold"),
            bg="#b91c1c",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.logout
        ).pack(fill="x", padx=12, pady=5)

        # Sidebar footer
        tk.Label(
            sidebar,
            text="Secure Banking Experience",
            font=("Arial", 9),
            bg="#142d4e",
            fg="#9bb5d1"
        ).pack(side="bottom", pady=20)

        # Top header
        header = tk.Frame(
            content,
            bg="#ffffff",
            height=75
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Banking Dashboard",
            font=("Arial", 21, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(side="left", padx=28, pady=18)

        tk.Label(
            header,
            text="SMART BANKING",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#3478b8"
        ).pack(side="right", padx=28)

        # Scrollable Dashboard Body
        body_container = tk.Frame(
            content,
            bg="#f1f5f9"
        )
        body_container.pack(fill="both", expand=True)

        body_canvas = tk.Canvas(
            body_container,
            bg="#f1f5f9",
            highlightthickness=0
        )
        body_canvas.pack(side="left", fill="both", expand=True)

        body_scrollbar = ttk.Scrollbar(
            body_container,
            orient="vertical",
            command=body_canvas.yview
        )
        body_scrollbar.pack(side="right", fill="y")

        body_canvas.configure(
            yscrollcommand=body_scrollbar.set
        )

        body = tk.Frame(
            body_canvas,
            bg="#f1f5f9"
        )

        body_window = body_canvas.create_window(
            (0, 0),
            window=body,
            anchor="nw"
        )

        body.bind(
            "<Configure>",
            lambda event: body_canvas.configure(
                scrollregion=body_canvas.bbox("all")
            )
        )

        body_canvas.bind(
            "<Configure>",
            lambda event: body_canvas.itemconfigure(
                body_window,
                width=event.width
            )
        )

        body_canvas.bind(
            "<MouseWheel>",
            lambda event: body_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

        
        tk.Label(
            body,
            text="Welcome to SBMS",
            font=("Arial", 24, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(anchor="w")

        tk.Label(
            body,
            text="Manage your banking operations from one place.",
            font=("Arial", 11),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(anchor="w", pady=(5, 25))

        # Welcome panel
        welcome = tk.Frame(
            body,
            bg="#24577a",
            height=155
        )
        welcome.pack(fill="x", pady=5)
        welcome.pack_propagate(False)

        tk.Label(
            welcome,
            text="Your Banking, Simplified.",
            font=("Arial", 23, "bold"),
            bg="#24577a",
            fg="white"
        ).pack(anchor="w", padx=25, pady=(30, 5))

        tk.Label(
            welcome,
            text="Access accounts, transactions and banking services easily.",
            font=("Arial", 11),
            bg="#24577a",
            fg="#e2edf7"
        ).pack(anchor="w", padx=25)
    # Dashboard Statistics
        stats = self.bank.get_dashboard_stats()

        if stats:
            stats_frame = tk.Frame(
                body,
                bg="#f1f5f9"
            )
            stats_frame.pack(fill="x", pady=(20, 5))

            cards = [
                ("Total Accounts", stats["total_accounts"]),
                ("Active Accounts    ", stats["active_accounts"]),
                ("Closed Accounts",stats["closed_accounts"]),
                ("Total Balance", f"₹ {stats['total_balance']:,.2f}"),
                ("Total Transactions", stats["total_transactions"]),
                ("Total Deposits", f"₹ {stats['total_deposits']:,.2f}"),
                ("Total Withdrawals", f"₹ {stats['total_withdrawals']:,.2f}")
            ]

            for index, (title, value) in enumerate(cards):

                card = tk.Frame(
                    stats_frame,
                    bg="white",
                    padx=15,
                    pady=18,
                    highlightbackground="#dbe4ee",
                    highlightthickness=1
                )

                card.grid(
                    row=0,
                    column=index,
                    padx=7,
                    pady=5,
                    sticky="nsew"
                )

                tk.Label(
                    card,
                    text=title,
                    font=("Arial", 10, "bold"),
                    bg="white",
                    fg="#64748b"
                ).pack(anchor="w")

                tk.Label(
                    card,
                    text=value,
                    font=("Arial", 19, "bold"),
                    bg="white",
                    fg="#24577a"
                ).pack(anchor="w", pady=(8, 0))

                stats_frame.grid_columnconfigure(index, weight=1)

        # Quick actions
        tk.Label(
            body,
            text="Quick Actions",
            font=("Arial", 17, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(anchor="w", pady=(28, 15))

        action_frame = tk.Frame(
            body,
            bg="#f1f5f9"
        )
        action_frame.pack(fill="x")

        quick_actions = [
            ("Create Account", self.create_account),
            ("Deposit Money", self.deposit),
            ("Withdraw Money", self.withdraw),
            ("Transfer Money", self.transfer_money)
        ]

        for index, (text, command) in enumerate(quick_actions):

            card = tk.Frame(
                action_frame,
                bg="white",
                padx=15,
                pady=20,
                highlightbackground="#dbe4ee",
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index,
                padx=7,
                pady=5,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=text,
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#24577a"
            ).pack(pady=5)

            tk.Button(
                card,
                text="Open",
                command=command,
                font=("Arial", 10, "bold"),
                bg="#24577a",
                fg="white",
                activebackground="#163d59",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                padx=18,
                pady=6
            ).pack(pady=5)

            action_frame.grid_columnconfigure(index, weight=1)
        # Recent Transactions Section
        tk.Label(
            body,
            text="Recent Transactions",
            font=("Arial", 17, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(anchor="w", pady=(25, 12))
        # Search and Filter Section
        search_frame = tk.Frame(
            body,
            bg="#f1f5f9"
        )
        search_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            search_frame,
            text="Search:",
            font=("Arial", 10, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(side="left", padx=(0, 8))

        search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            width=25,
            relief="solid",
            bd=1
        )
        search_entry.pack(side="left", padx=5, ipady=6)

        tk.Label(
            search_frame,
            text="Transaction Type:",
            font=("Arial", 10, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(side="left", padx=(15, 5))

        filter_combo = ttk.Combobox(
            search_frame,
            values=[
                "All",
                "Deposit",
                "Withdraw",
                "Transfer money",
                "Received money"
            ],
            state="readonly",
            width=18,
            font=("Arial", 10)
        )
        filter_combo.set("All")
        filter_combo.pack(side="left", padx=5, ipady=4)

        recent_frame = tk.Frame(
            body,
            bg="white",
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        recent_frame.pack(fill="x", pady=5)

        columns = (
            "Transaction ID",
            "Customer Name",
            "Account Number",
            "Type",
            "Amount",
            "Date & Time"
        )
        # Recent Transactions Table Styling
        recent_style = ttk.Style()
        recent_style.theme_use("clam")

        recent_style.configure(
            "Recent.Treeview",
            background="white",
            foreground="#142d4e",
            rowheight=30,
            font=("Arial", 10),
            fieldbackground="white"
        )

        recent_style.configure(
            "Recent.Treeview.Heading",
            background="#24577a",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=8
        )

        recent_style.map(
            "Recent.Treeview",
            background=[("selected", "#3478b8")],
            foreground=[("selected", "white")]
        )

        recent_table = ttk.Treeview(
            recent_frame,
            columns=columns,
            show="headings",
            height=5,
            style="Recent.Treeview"
        )

        for column in columns:
            recent_table.heading(
                column,
                text=column
            )

            recent_table.column(
                column,
                anchor="center",
                width=140
            )

        recent_table.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8,
            pady=8
        )

        recent_scrollbar = ttk.Scrollbar(
            recent_frame,
            orient="vertical",
            command=recent_table.yview
        )
        recent_scrollbar.pack(side="right", fill="y")

        recent_table.configure(
            yscrollcommand=recent_scrollbar.set
        )

        # Fetch all transactions
        transactions = self.bank.get_recent_transactions()

        def display_transactions():

            recent_table.delete(*recent_table.get_children())

            search_text = search_entry.get().strip().lower()
            selected_type = filter_combo.get()

            if transactions:
                for transaction in transactions:

                    customer_name = str(transaction[1]).lower()
                    account_number = str(transaction[2])
                    transaction_type = transaction[3]

                    # Search by customer name or account number
                    if (
                        search_text
                        and search_text not in customer_name
                        and search_text not in account_number
                    ):
                        continue

                    # Filter by transaction type
                    if (
                        selected_type != "All"
                        and transaction_type != selected_type
                    ):
                        continue

                    recent_table.insert(
                        "",
                        "end",
                        values=(
                            transaction[0],
                            transaction[1],
                            transaction[2],
                            transaction[3],
                            f"₹ {transaction[4]:,.2f}",
                            transaction[5]
                        )
                    )

        def reset_transaction_filters():
            search_entry.delete(0, tk.END)
            filter_combo.set("All")
            display_transactions()

        # Search Button
        tk.Button(
            search_frame,
            text="Search",
            command=display_transactions,
            bg="#24577a",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        ).pack(side="left", padx=5)

        # Reset Button
        tk.Button(
            search_frame,
            text="Reset",
            command=reset_transaction_filters,
            bg="#64748b",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6
        ).pack(side="left", padx=5)

        # Press Enter to search
        search_entry.bind(
            "<Return>",
            lambda event: display_transactions()
        )

        # Display all transactions initially
        display_transactions()

        # Footer
        tk.Label(
            body,
            text="SBMS  |  Secure • Reliable • Always With You",
            font=("Arial", 9),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(side="bottom", pady=10)

    def create_account(self):

        # Main Window
        window = tk.Toplevel(self.root)
        window.title("SBMS - Create New Account")
        window.geometry("750x600")
        window.minsize(650, 550)
        window.configure(bg="#f1f5f9")
    
        # Header
        header = tk.Frame(
            window,
            bg="#142d4e",
            height=100
        )
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="CREATE NEW ACCOUNT",
            font=("Arial", 22, "bold"),
            bg="#142d4e",
            fg="white"
        ).pack(anchor="w", padx=28, pady=(20, 4))
    
        tk.Label(
            header,
            text="Register a New Banking Customer",
            font=("Arial", 11),
            bg="#142d4e",
            fg="#cbddec"
        ).pack(anchor="w", padx=30)
    
        # Content
        content = tk.Frame(
            window,
            bg="#f1f5f9"
        )
        content.pack(fill="both", expand=True, padx=35, pady=25)
    
        # Account Information Card
        info_card = tk.Frame(
            content,
            bg="white",
            padx=25,
            pady=20,
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        info_card.pack(fill="x", pady=(0, 20))
    
        tk.Label(
            info_card,
            text="ACCOUNT INFORMATION",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w")
    
        tk.Label(
            info_card,
            text="Account Number will be generated automatically.",
            font=("Arial", 12),
            bg="white",
            fg="#24577a"
        ).pack(anchor="w", pady=(12, 5))
    
        # Customer Form
        form_card = tk.Frame(
            content,
            bg="white",
            padx=25,
            pady=22,
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        form_card.pack(fill="x")
    
        # Customer Name
        tk.Label(
            form_card,
            text="Customer Name",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(anchor="w")
    
        name_entry = tk.Entry(
            form_card,
            font=("Arial", 13),
            relief="solid",
            bd=1
        )
        name_entry.pack(fill="x", ipady=9, pady=(10, 18))
        name_entry.focus_set()
    
        # Initial Deposit
        tk.Label(
            form_card,
            text="Initial Deposit (₹)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(anchor="w")
    
        balance_entry = tk.Entry(
            form_card,
            font=("Arial", 13),
            relief="solid",
            bd=1
        )
        balance_entry.pack(fill="x", ipady=9, pady=(10, 18))
        balance_entry.insert(0, "0")
    
        # Create Account Function
        def save_account():
    
            name = name_entry.get().strip()
            balance_text = balance_entry.get().strip()
    
            if not name:
                messagebox.showwarning(
                    "Invalid Name",
                    "Please enter customer name.",
                    parent=window
                )
                name_entry.focus_set()
                return
    
            try:
                balance = float(balance_text)
    
                if balance < 0:
                    raise ValueError
    
            except ValueError:
                messagebox.showwarning(
                    "Invalid Deposit",
                    "Please enter a valid non-negative deposit amount.",
                    parent=window
                )
                balance_entry.focus_set()
                return
    
            account_number = self.bank.create_account(
                name,
                balance
            )
    
            if account_number is not None:
                # Save Account Creation Activity
                self.bank.database.log_activity(
                    self.admin_username,
                    "Create Account",
                    f"Created account {account_number} for {name}"
                )
    
                messagebox.showinfo(
                    "Account Created Successfully",
                    f"New account has been created successfully!\n\n"
                    f"Customer Name: {name}\n"
                    f"Account Number: {account_number}\n"
                    f"Initial Balance: ₹ {balance:,.2f}",
                    parent=window
                )
    
                window.destroy()
    
            else:
    
                messagebox.showerror(
                    "Account Creation Failed",
                    "Unable to create account. Please try again.",
                    parent=window
                )
    
        # Create Button
        tk.Button(
            form_card,
            text="CREATE ACCOUNT",
            command=save_account,
            font=("Arial", 11, "bold"),
            bg="#24577a",
            fg="white",
            activebackground="#142d4e",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=12
        ).pack(anchor="w")
    
        # Footer
        tk.Label(
            content,
            text="SBMS  |  Secure • Reliable • Professional Banking",
            font=("Arial", 9),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(pady=(15, 0))

    def deposit(self):

        window = tk.Toplevel(self.root)
        window.title("Deposit Money")
        window.geometry("520x570")
        window.configure(bg="#f4f7fb")
        window.resizable(False, False)
    
        # Header
        header = tk.Frame(window, bg="#142d4e", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="DEPOSIT MONEY",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#142d4e"
        ).pack(pady=(20, 5))
    
        tk.Label(
            header,
            text="Add funds to an active customer account",
            font=("Segoe UI", 10),
            fg="#d5e2f2",
            bg="#142d4e"
        ).pack()
    
        # Main form
        form = tk.Frame(window, bg="white", padx=28, pady=22)
        form.pack(fill="both", expand=True, padx=25, pady=22)
    
        tk.Label(
            form,
            text="Account Number",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w")
    
        account_entry = tk.Entry(
            form,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )
        account_entry.pack(fill="x", pady=(7, 8), ipady=7)
    
        # Customer details
        details = tk.Frame(form, bg="#f1f5fa", padx=15, pady=12)
        details.pack(fill="x", pady=8)
    
        name_label = tk.Label(
            details,
            text="Customer Name: --",
            font=("Segoe UI", 10),
            bg="#f1f5fa",
            fg="#26364a"
        )
        name_label.pack(anchor="w", pady=3)
    
        balance_label = tk.Label(
            details,
            text="Current Balance: --",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5fa",
            fg="#1673b1"
        )
        balance_label.pack(anchor="w", pady=3)
    
        account_status = tk.Label(
            details,
            text="Account Status: --",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5fa",
            fg="#26364a"
        )
        account_status.pack(anchor="w", pady=3)
    
        account_data = {"account": None}
    
        def verify_account():
    
            account_number = account_entry.get().strip()
    
            if not account_number.isdigit():
                messagebox.showwarning(
                    "Invalid Account",
                    "Please enter a valid account number.",
                    parent=window
                )
                return
    
            account = self.bank.search_account(account_number)
    
            if account is None:
                account_data["account"] = None
                name_label.config(text="Customer Name: --")
                balance_label.config(text="Current Balance: --")
                account_status.config(text="Account Status: Not Found")
                return
    
            status = self.bank.get_account_status(account_number)
    
            account_data["account"] = account
    
            name_label.config(text=f"Customer Name: {account[1]}")
            balance_label.config(
                text=f"Current Balance: ₹ {account[2]:,.2f}"
            )
            account_status.config(
                text=f"Account Status: {status}",
                fg="#16834a" if status == "Active" else "#d93025"
            )
    
        tk.Button(
            form,
            text="VERIFY ACCOUNT",
            font=("Segoe UI", 9, "bold"),
            bg="#e5edf7",
            fg="#173b63",
            relief="flat",
            cursor="hand2",
            command=verify_account
        ).pack(fill="x", pady=5, ipady=7)
    
        # Deposit amount
        tk.Label(
            form,
            text="Deposit Amount (₹)",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w", pady=(15, 5))
    
        amount_entry = tk.Entry(
            form,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )
        amount_entry.pack(fill="x", ipady=7)
    
        def confirm_deposit():
    
            account = account_data["account"]
    
            if account is None:
                messagebox.showwarning(
                    "Verify Account",
                    "Please verify the account first.",
                    parent=window
                )
                return
    
            account_number = account[0]
            amount_text = amount_entry.get().strip()
    
            try:
                amount = float(amount_text)
            except ValueError:
                messagebox.showwarning(
                    "Invalid Amount",
                    "Please enter a valid deposit amount.",
                    parent=window
                )
                return
    
            if amount <= 0:
                messagebox.showwarning(
                    "Invalid Amount",
                    "Deposit amount must be greater than zero.",
                    parent=window
                )
                return
    
            if not self.bank.deposit(account_number, amount):
                messagebox.showerror(
                    "Deposit Failed",
                    "Deposit could not be completed.\n"
                    "Please check the account status and try again.",
                    parent=window
                )
                return
    
            updated_account = self.bank.search_account(account_number)
            # Save Deposit Activity
            self.bank.database.log_activity(
                self.admin_username,
                "Deposit",
                f"Deposited ₹{amount:,.2f} into account {account_number}"
            )
    
            messagebox.showinfo(
                "Deposit Successful",
                f"Money deposited successfully!\n\n"
                f"Customer: {updated_account[1]}\n"
                f"Account Number: {account_number}\n"
                f"Deposited Amount: ₹ {amount:,.2f}\n"
                f"Updated Balance: ₹ {updated_account[2]:,.2f}",
                parent=window
            )
    
            balance_label.config(
                text=f"Current Balance: ₹ {updated_account[2]:,.2f}"
            )
            amount_entry.delete(0, tk.END)
    
        tk.Button(
            form,
            text="DEPOSIT MONEY",
            font=("Segoe UI", 11, "bold"),
            bg="#1673b1",
            fg="white",
            activebackground="#105b90",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=confirm_deposit
        ).pack(fill="x", pady=(22, 5), ipady=10)

    def withdraw(self):

        window = tk.Toplevel(self.root)
        window.title("Withdraw Money")
        window.geometry("520x570")
        window.configure(bg="#f4f7fb")
        window.resizable(False, False)
    
        # Header
        header = tk.Frame(window, bg="#142d4e", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="WITHDRAW MONEY",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#142d4e"
        ).pack(pady=(20, 5))
    
        tk.Label(
            header,
            text="Withdraw funds from an active customer account",
            font=("Segoe UI", 10),
            fg="#d5e2f2",
            bg="#142d4e"
        ).pack()
    
        # Main Form
        form = tk.Frame(window, bg="white", padx=28, pady=22)
        form.pack(fill="both", expand=True, padx=25, pady=22)
    
        tk.Label(
            form,
            text="Account Number",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w")
    
        account_entry = tk.Entry(
            form,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )
        account_entry.pack(fill="x", pady=(7, 8), ipady=7)
    
        # Customer Details
        details = tk.Frame(
            form,
            bg="#f1f5fa",
            padx=15,
            pady=12
        )
        details.pack(fill="x", pady=8)
    
        name_label = tk.Label(
            details,
            text="Customer Name: --",
            font=("Segoe UI", 10),
            bg="#f1f5fa",
            fg="#26364a"
        )
        name_label.pack(anchor="w", pady=3)
    
        balance_label = tk.Label(
            details,
            text="Current Balance: --",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5fa",
            fg="#1673b1"
        )
        balance_label.pack(anchor="w", pady=3)
    
        account_status = tk.Label(
            details,
            text="Account Status: --",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5fa",
            fg="#26364a"
        )
        account_status.pack(anchor="w", pady=3)
    
        account_data = {"account": None}
    
        # Verify Account
        def verify_account():
    
            account_number = account_entry.get().strip()
    
            if not account_number.isdigit():
                account_data["account"] = None
                messagebox.showwarning(
                    "Invalid Account",
                    "Please enter a valid account number.",
                    parent=window
                )
                return
    
            account = self.bank.search_account(account_number)
    
            if account is None:
                account_data["account"] = None
                name_label.config(text="Customer Name: --")
                balance_label.config(text="Current Balance: --")
                account_status.config(text="Account Status: Not Found")
                return
    
            status = self.bank.get_account_status(account_number)
    
            account_data["account"] = account
    
            name_label.config(text=f"Customer Name: {account[1]}")
            balance_label.config(
                text=f"Current Balance: ₹ {account[2]:,.2f}"
            )
            account_status.config(
                text=f"Account Status: {status}",
                fg="#16834a" if status == "Active" else "#d93025"
            )
    
        tk.Button(
            form,
            text="VERIFY ACCOUNT",
            font=("Segoe UI", 9, "bold"),
            bg="#e5edf7",
            fg="#173b63",
            relief="flat",
            cursor="hand2",
            command=verify_account
        ).pack(fill="x", pady=5, ipady=7)
    
        # Withdrawal Amount
        tk.Label(
            form,
            text="Withdrawal Amount (₹)",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w", pady=(15, 5))
    
        amount_entry = tk.Entry(
            form,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )
        amount_entry.pack(fill="x", ipady=7)
    
        # Confirm Withdrawal
        def confirm_withdrawal():
    
            account = account_data["account"]
    
            if account is None:
                messagebox.showwarning(
                    "Verify Account",
                    "Please verify the account first.",
                    parent=window
                )
                return
    
            account_number = account[0]
            amount_text = amount_entry.get().strip()
    
            try:
                amount = float(amount_text)
            except ValueError:
                messagebox.showwarning(
                    "Invalid Amount",
                    "Please enter a valid withdrawal amount.",
                    parent=window
                )
                return
    
            if amount <= 0:
                messagebox.showwarning(
                    "Invalid Amount",
                    "Withdrawal amount must be greater than zero.",
                    parent=window
                )
                return
    
            if amount > account[2]:
                messagebox.showwarning(
                    "Insufficient Balance",
                    f"Available Balance: ₹ {account[2]:,.2f}\n\n"
                    "You cannot withdraw more than your available balance.",
                    parent=window
                )
                return
    
            if not self.bank.withdraw(account_number, amount):
                messagebox.showerror(
                    "Withdrawal Failed",
                    "Withdrawal could not be completed.\n"
                    "Please check the account status and try again.",
                    parent=window
                )
                return
    
            updated_account = self.bank.search_account(account_number)
            # Save Withdrawal Activity
            self.bank.database.log_activity(
                self.admin_username,
                "Withdraw",
                f"Withdrawn ₹{amount:,.2f} from account {account_number}"
            )
    
            messagebox.showinfo(
                "Withdrawal Successful",
                f"Withdrawal completed successfully!\n\n"
                f"Customer: {updated_account[1]}\n"
                f"Account Number: {account_number}\n"
                f"Withdrawn Amount: ₹ {amount:,.2f}\n"
                f"Remaining Balance: ₹ {updated_account[2]:,.2f}",
                parent=window
            )
    
            account_data["account"] = updated_account
    
            balance_label.config(
                text=f"Current Balance: ₹ {updated_account[2]:,.2f}"
            )
    
            amount_entry.delete(0, tk.END)
    
        tk.Button(
            form,
            text="WITHDRAW MONEY",
            font=("Segoe UI", 11, "bold"),
            bg="#1673b1",
            fg="white",
            activebackground="#105b90",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=confirm_withdrawal
        ).pack(fill="x", pady=(22, 5), ipady=10)
    
    def check_balance(self):

        window = tk.Toplevel(self.root)
        window.title("Check Account Balance")
        window.geometry("500x540")
        window.configure(bg="#f4f7fb")
        window.resizable(False, False)
    
        # Header
        header = tk.Frame(window, bg="#142d4e", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="ACCOUNT BALANCE",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#142d4e"
        ).pack(pady=(20, 5))
    
        tk.Label(
            header,
            text="View customer account balance and details",
            font=("Segoe UI", 10),
            fg="#d5e2f2",
            bg="#142d4e"
        ).pack()
    
        # Main Form
        form = tk.Frame(window, bg="white", padx=25, pady=22)
        form.pack(fill="both", expand=True, padx=25, pady=22)
    
        tk.Label(
            form,
            text="Account Number",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w")
    
        account_entry = tk.Entry(
            form,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )
        account_entry.pack(fill="x", pady=(8, 12), ipady=7)
    
        # Account Details Card
        details = tk.Frame(
            form,
            bg="#f1f5fa",
            padx=18,
            pady=15
        )
        details.pack(fill="x", pady=8)
    
        name_label = tk.Label(
            details,
            text="Customer Name: --",
            font=("Segoe UI", 10),
            bg="#f1f5fa",
            fg="#26364a"
        )
        name_label.pack(anchor="w", pady=5)
    
        number_label = tk.Label(
            details,
            text="Account Number: --",
            font=("Segoe UI", 10),
            bg="#f1f5fa",
            fg="#26364a"
        )
        number_label.pack(anchor="w", pady=5)
    
        status_label = tk.Label(
            details,
            text="Account Status: --",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5fa",
            fg="#26364a"
        )
        status_label.pack(anchor="w", pady=5)
    
        balance_label = tk.Label(
            details,
            text="₹ 0.00",
            font=("Segoe UI", 22, "bold"),
            bg="#f1f5fa",
            fg="#1673b1"
        )
        balance_label.pack(anchor="center", pady=(12, 5))
    
        tk.Label(
            details,
            text="AVAILABLE ACCOUNT BALANCE",
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5fa",
            fg="#718096"
        ).pack(anchor="center")
    
        # Verify Account
        def verify_account():
    
            account_number = account_entry.get().strip()
    
            if not account_number.isdigit():
                messagebox.showwarning(
                    "Invalid Account",
                    "Please enter a valid account number.",
                    parent=window
                )
                return
    
            account = self.bank.search_account(account_number)
    
            if account is None:
                name_label.config(text="Customer Name: --")
                number_label.config(text="Account Number: --")
                status_label.config(text="Account Status: Not Found")
                balance_label.config(text="₹ 0.00")
    
                messagebox.showerror(
                    "Account Not Found",
                    "No account found with this account number.",
                    parent=window
                )
                return
    
            status = self.bank.get_account_status(account_number)
    
            name_label.config(text=f"Customer Name: {account[1]}")
            number_label.config(text=f"Account Number: {account[0]}")
    
            status_label.config(
                text=f"Account Status: {status}",
                fg="#16834a" if status == "Active" else "#d93025"
            )
    
            balance_label.config(
                text=f"₹ {account[2]:,.2f}"
            )
    
        tk.Button(
            form,
            text="CHECK BALANCE",
            font=("Segoe UI", 11, "bold"),
            bg="#1673b1",
            fg="white",
            activebackground="#105b90",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=verify_account
        ).pack(fill="x", pady=(12, 3), ipady=9)
    
        account_entry.focus_set()

    def transaction_history(self):

        account = simpledialog.askinteger(
            "Transaction History",
            "Enter Account Number:",
            parent=self.root
        )

        if account is None:
            return

        transactions = self.bank.transaction_history(account)

        if not transactions:
            messagebox.showinfo(
                "Transaction History",
                "No transactions found for this account."
            )
            return

        summary = self.bank.get_account_summary(account)

        if summary is None:
            messagebox.showerror(
                "Error",
                "Unable to fetch account summary."
            )
            return

        name, balance, deposits, withdrawals, total_txns = summary

        # Main Window
        window = tk.Toplevel(self.root)
        window.title("SBMS - Transaction History")
        window.geometry("1050x650")
        window.minsize(850, 500)
        window.configure(bg="#f1f5f9")

        # Header
        header = tk.Frame(window, bg="#142d4e", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="TRANSACTION HISTORY",
            font=("Arial", 22, "bold"),
            bg="#142d4e",
            fg="white"
        ).pack(anchor="w", padx=25, pady=(15, 3))

        tk.Label(
            header,
            text=f"Customer: {name}  |  Account Number: {account}",
            font=("Arial", 11),
            bg="#142d4e",
            fg="#cbddec"
        ).pack(anchor="w", padx=27)

        # Main Content
        content = tk.Frame(window, bg="#f1f5f9")
        content.pack(fill="both", expand=True, padx=22, pady=18)

        tk.Label(
            content,
            text="Transaction Overview",
            font=("Arial", 17, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(anchor="w", pady=(0, 12))

        # Summary Cards
        summary_frame = tk.Frame(content, bg="#f1f5f9")
        summary_frame.pack(fill="x", pady=(0, 22))

        cards = [
            ("Current Balance", f"₹ {balance:,.2f}"),
            ("Total Deposits", f"₹ {deposits:,.2f}"),
            ("Total Withdrawals", f"₹ {withdrawals:,.2f}"),
            ("Total Transactions", str(total_txns))
        ]

        for index, (title, value) in enumerate(cards):

            card = tk.Frame(
                summary_frame,
                bg="white",
                padx=15,
                pady=18,
                highlightbackground="#dbe4ee",
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index,
                padx=6,
                pady=5,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=title,
                font=("Arial", 9, "bold"),
                bg="white",
                fg="#64748b"
            ).pack(anchor="w")

            tk.Label(
                card,
                text=value,
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#24577a"
            ).pack(anchor="w", pady=(10, 0))

            summary_frame.grid_columnconfigure(index, weight=1)

        # Table Heading
        tk.Label(
            content,
            text="All Transactions",
            font=("Arial", 17, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(anchor="w", pady=(0, 12))

        # Table Container
        table_frame = tk.Frame(
            content,
            bg="white",
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True)

        columns = (
            "Transaction ID",
            "Transaction Type",
            "Amount",
            "Date & Time"
        )

        history_style = ttk.Style()

        history_style.configure(
            "History.Treeview",
            background="white",
            foreground="#142d4e",
            rowheight=34,
            font=("Arial", 10),
            fieldbackground="white"
        )

        history_style.configure(
            "History.Treeview.Heading",
            background="#24577a",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=9
        )

        history_style.map(
            "History.Treeview",
            background=[("selected", "#3478b8")],
            foreground=[("selected", "white")]
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="History.Treeview"
        )

        column_widths = {
            "Transaction ID": 200,
            "Transaction Type": 220,
            "Amount": 180,
            "Date & Time": 300
        }

        for column in columns:
            tree.heading(column, text=column)
            tree.column(
                column,
                width=column_widths[column],
                minwidth=120,
                anchor="center"
            )

        # Insert Transactions
        for txn in transactions:
            tree.insert(
                "",
                "end",
                values=(
                    txn[0],
                    txn[1],
                    f"₹ {txn[2]:,.2f}",
                    txn[3]
                )
            )

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        vertical_scrollbar.pack(side="right", fill="y")
        horizontal_scrollbar.pack(side="bottom", fill="x")

        tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # Footer
        tk.Label(
            content,
            text="SBMS  |  Secure • Reliable • Professional Banking",
            font=("Arial", 9),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(pady=(12, 0))
        
    def transfer_money(self):

        window = tk.Toplevel(self.root)
        window.title("Transfer Money")
        window.geometry("600x680")
        window.configure(bg="#f4f7fb")
        window.resizable(False, False)
    
        # Header
        header = tk.Frame(window, bg="#142d4e", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="TRANSFER MONEY",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#142d4e"
        ).pack(pady=(20, 5))
    
        tk.Label(
            header,
            text="Transfer funds securely between customer accounts",
            font=("Segoe UI", 10),
            fg="#d5e2f2",
            bg="#142d4e"
        ).pack()
    
        # Main Form
        form = tk.Frame(window, bg="white", padx=25, pady=8)
        form.pack(fill="both", expand=True, padx=22, pady=18)
    
        # Account Details Card
        def create_account_card(title, color):
    
            card = tk.LabelFrame(
                form,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bg="#f1f5fa",
                fg=color,
                padx=12,
                pady=8
            )
            card.pack(fill="x", pady=3)
    
            name_label = tk.Label(
                card,
                text="Customer Name: --",
                font=("Segoe UI", 9),
                bg="#f1f5fa",
                fg="#26364a"
            )
            name_label.pack(anchor="w", pady=2)
    
            balance_label = tk.Label(
                card,
                text="Current Balance: --",
                font=("Segoe UI", 9, "bold"),
                bg="#f1f5fa",
                fg="#1673b1"
            )
            balance_label.pack(anchor="w", pady=2)
    
            status_label = tk.Label(
                card,
                text="Account Status: --",
                font=("Segoe UI", 9, "bold"),
                bg="#f1f5fa",
                fg="#26364a"
            )
            status_label.pack(anchor="w", pady=2)
    
            return name_label, balance_label, status_label
    
        # Sender Section
        tk.Label(
            form,
            text="Sender Account Number",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w")
    
        sender_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )
        sender_entry.pack(fill="x", pady=(5, 2), ipady=6)
    
        sender_name, sender_balance, sender_status = (
            create_account_card("SENDER DETAILS", "#1673b1")
        )
    
        # Receiver Section
        tk.Label(
            form,
            text="Receiver Account Number",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w", pady=(8, 0))
    
        receiver_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )
        receiver_entry.pack(fill="x", pady=(5, 2), ipady=6)
    
        receiver_name, receiver_balance, receiver_status = (
            create_account_card("RECEIVER DETAILS", "#16834a")
        )
    
        sender_data = {"account": None}
        receiver_data = {"account": None}
    
        # Verify Sender
        def verify_sender():
    
            account_number = sender_entry.get().strip()
    
            sender_data["account"] = None
            sender_name.config(text="Customer Name: --")
            sender_balance.config(text="Current Balance: --")
            sender_status.config(text="Account Status: --")
    
            if not account_number.isdigit():
                messagebox.showwarning(
                    "Invalid Account",
                    "Please enter a valid sender account number.",
                    parent=window
                )
                return
    
            account = self.bank.search_account(account_number)
    
            if account is None:
                sender_status.config(text="Account Status: Not Found")
                return
    
            status = self.bank.get_account_status(account_number)
            sender_data["account"] = account
    
            sender_name.config(text=f"Customer Name: {account[1]}")
            sender_balance.config(
                text=f"Current Balance: ₹ {account[2]:,.2f}"
            )
            sender_status.config(
                text=f"Account Status: {status}",
                fg="#16834a" if status == "Active" else "#d93025"
            )
    
        # Verify Receiver
        def verify_receiver():
    
            account_number = receiver_entry.get().strip()
    
            receiver_data["account"] = None
            receiver_name.config(text="Customer Name: --")
            receiver_balance.config(text="Current Balance: --")
            receiver_status.config(text="Account Status: --")
    
            if not account_number.isdigit():
                messagebox.showwarning(
                    "Invalid Account",
                    "Please enter a valid receiver account number.",
                    parent=window
                )
                return
    
            account = self.bank.search_account(account_number)
    
            if account is None:
                receiver_status.config(text="Account Status: Not Found")
                return
    
            status = self.bank.get_account_status(account_number)
            receiver_data["account"] = account
    
            receiver_name.config(text=f"Customer Name: {account[1]}")
            receiver_balance.config(
                text=f"Current Balance: ₹ {account[2]:,.2f}"
            )
            receiver_status.config(
                text=f"Account Status: {status}",
                fg="#16834a" if status == "Active" else "#d93025"
            )
    
        # Verification Buttons
        tk.Button(
            form,
            text="VERIFY SENDER",
            font=("Segoe UI", 8, "bold"),
            bg="#e5edf7",
            fg="#173b63",
            relief="flat",
            cursor="hand2",
            command=verify_sender
        ).pack(fill="x", pady=3, ipady=5)
    
        tk.Button(
            form,
            text="VERIFY RECEIVER",
            font=("Segoe UI", 8, "bold"),
            bg="#e5edf7",
            fg="#173b63",
            relief="flat",
            cursor="hand2",
            command=verify_receiver
        ).pack(fill="x", pady=3, ipady=5)
    
        # Transfer Amount
        tk.Label(
            form,
            text="Transfer Amount (₹)",
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w", pady=(10, 4))
    
        amount_entry = tk.Entry(
            form,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )
        amount_entry.pack(fill="x", ipady=6)
    
        # Confirm Transfer
        def confirm_transfer():
    
            sender = sender_data["account"]
            receiver = receiver_data["account"]
    
            if sender is None or receiver is None:
                messagebox.showwarning(
                    "Verify Accounts",
                    "Please verify both sender and receiver accounts.",
                    parent=window
                )
                return
    
            sender_number = sender[0]
            receiver_number = receiver[0]
    
            if sender_number == receiver_number:
                messagebox.showwarning(
                    "Invalid Transfer",
                    "Sender and receiver accounts must be different.",
                    parent=window
                )
                return
    
            amount_text = amount_entry.get().strip()
    
            try:
                amount = float(amount_text)
            except ValueError:
                messagebox.showwarning(
                    "Invalid Amount",
                    "Please enter a valid transfer amount.",
                    parent=window
                )
                return
    
            if amount <= 0:
                messagebox.showwarning(
                    "Invalid Amount",
                    "Transfer amount must be greater than zero.",
                    parent=window
                )
                return
    
            if amount > sender[2]:
                messagebox.showwarning(
                    "Insufficient Balance",
                    f"Available Balance: ₹ {sender[2]:,.2f}\n\n"
                    "Sender does not have sufficient balance.",
                    parent=window
                )
                return
    
            if not self.bank.transfer(
                sender_number,
                receiver_number,
                amount
            ):
                messagebox.showerror(
                    "Transfer Failed",
                    "Transfer could not be completed.\n"
                    "Please check account status and try again.",
                    parent=window
                )
                return
    
            updated_sender = self.bank.search_account(sender_number)
            updated_receiver = self.bank.search_account(receiver_number)
            # Save Transfer Activity
            self.bank.database.log_activity(
                self.admin_username,
                "Transfer",
                f"Transferred ₹{amount:,.2f} from account "
                f"{sender_number} to account {receiver_number}"
            )
    
            messagebox.showinfo(
                "Transfer Successful",
                f"Money transferred successfully!\n\n"
                f"Sender: {updated_sender[1]}\n"
                f"Sender Account: {sender_number}\n"
                f"Receiver: {updated_receiver[1]}\n"
                f"Receiver Account: {receiver_number}\n"
                f"Transferred Amount: ₹ {amount:,.2f}\n\n"
                f"Sender Balance: ₹ {updated_sender[2]:,.2f}\n"
                f"Receiver Balance: ₹ {updated_receiver[2]:,.2f}",
                parent=window
            )
    
            sender_data["account"] = updated_sender
            receiver_data["account"] = updated_receiver
    
            sender_balance.config(
                text=f"Current Balance: ₹ {updated_sender[2]:,.2f}"
            )
            receiver_balance.config(
                text=f"Current Balance: ₹ {updated_receiver[2]:,.2f}"
            )
    
            amount_entry.delete(0, tk.END)
    
        tk.Button(
            form,
            text="TRANSFER MONEY",
            font=("Segoe UI", 11, "bold"),
            bg="#1673b1",
            fg="white",
            activebackground="#105b90",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=confirm_transfer
        ).pack(fill="x", pady=(8, 2), ipady=6)
        
    def close_account(self):

        window = tk.Toplevel(self.root)
        window.title("Close Customer Account")
        window.geometry("520x650")
        window.configure(bg="#f4f7fb")
        window.resizable(False, False)
    
        # Header
        header = tk.Frame(window, bg="#142d4e", height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
    
        tk.Label(
            header,
            text="ACCOUNT CLOSURE",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#142d4e"
        ).pack(pady=(20, 5))
    
        tk.Label(
            header,
            text="Manage customer account closure securely",
            font=("Segoe UI", 10),
            fg="#d5e2f2",
            bg="#142d4e"
        ).pack()
    
        # Main Form
        form = tk.Frame(window, bg="white", padx=28, pady=22)
        form.pack(fill="both", expand=True, padx=25, pady=22)
    
        tk.Label(
            form,
            text="Account Number",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#26364a"
        ).pack(anchor="w")
    
        account_entry = tk.Entry(
            form,
            font=("Segoe UI", 12),
            relief="solid",
            bd=1
        )
        account_entry.pack(fill="x", pady=(8, 10), ipady=7)
    
        # Account Details
        details = tk.Frame(
            form,
            bg="#f1f5fa",
            padx=18,
            pady=15
        )
        details.pack(fill="x", pady=8)
    
        name_label = tk.Label(
            details,
            text="Customer Name: --",
            font=("Segoe UI", 10),
            bg="#f1f5fa",
            fg="#26364a"
        )
        name_label.pack(anchor="w", pady=5)
    
        number_label = tk.Label(
            details,
            text="Account Number: --",
            font=("Segoe UI", 10),
            bg="#f1f5fa",
            fg="#26364a"
        )
        number_label.pack(anchor="w", pady=5)
    
        status_label = tk.Label(
            details,
            text="Account Status: --",
            font=("Segoe UI", 10, "bold"),
            bg="#f1f5fa",
            fg="#26364a"
        )
        status_label.pack(anchor="w", pady=5)
    
        balance_label = tk.Label(
            details,
            text="₹ 0.00",
            font=("Segoe UI", 22, "bold"),
            bg="#f1f5fa",
            fg="#1673b1"
        )
        balance_label.pack(anchor="center", pady=(12, 5))
    
        tk.Label(
            details,
            text="CURRENT ACCOUNT BALANCE",
            font=("Segoe UI", 8, "bold"),
            bg="#f1f5fa",
            fg="#718096"
        ).pack(anchor="center")
    
        account_data = {"account": None}
    
        # Reset Details
        def reset_details():
    
            account_data["account"] = None
    
            name_label.config(text="Customer Name: --")
            number_label.config(text="Account Number: --")
            status_label.config(text="Account Status: --")
            balance_label.config(text="₹ 0.00")
    
        # Verify Account
        def verify_account():
    
            account_number = account_entry.get().strip()
    
            reset_details()
    
            if not account_number.isdigit():
                messagebox.showwarning(
                    "Invalid Account",
                    "Please enter a valid account number.",
                    parent=window
                )
                return
    
            account = self.bank.search_account(account_number)
    
            if account is None:
                status_label.config(text="Account Status: Not Found")
    
                messagebox.showerror(
                    "Account Not Found",
                    "No account found with this account number.",
                    parent=window
                )
                return
    
            status = self.bank.get_account_status(account_number)
    
            if status not in ("Active", "Closed"):
                messagebox.showerror(
                    "Error",
                    "Unable to verify account status.",
                    parent=window
                )
                return
    
            account_data["account"] = account
    
            name_label.config(text=f"Customer Name: {account[1]}")
            number_label.config(text=f"Account Number: {account[0]}")
    
            status_label.config(
                text=f"Account Status: {status}",
                fg="#16834a" if status == "Active" else "#d93025"
            )
    
            balance_label.config(
                text=f"₹ {account[2]:,.2f}"
            )
    
        # Verify Button
        tk.Button(
            form,
            text="VERIFY ACCOUNT",
            font=("Segoe UI", 9, "bold"),
            bg="#e5edf7",
            fg="#173b63",
            relief="flat",
            cursor="hand2",
            command=verify_account
        ).pack(fill="x", pady=5, ipady=7)
    
        # Warning
        tk.Label(
            form,
            text="Note: Account must have zero balance before closure.",
            font=("Segoe UI", 9),
            bg="white",
            fg="#bd6b13",
            wraplength=400
        ).pack(anchor="w", pady=(10, 5))
    
        # Close Account
        def confirm_closure():
    
            account = account_data["account"]
    
            if account is None:
                messagebox.showwarning(
                    "Verify Account",
                    "Please verify the account first.",
                    parent=window
                )
                return
    
            account_number = account[0]
    
            # Fetch latest account details
            latest_account = self.bank.search_account(account_number)
    
            if latest_account is None:
                reset_details()
                messagebox.showerror(
                    "Account Not Found",
                    "Account no longer exists.",
                    parent=window
                )
                return
    
            name = latest_account[1]
            balance = latest_account[2]
            status = self.bank.get_account_status(account_number)
    
            if status == "Closed":
                messagebox.showwarning(
                    "Already Closed",
                    "This account is already closed.",
                    parent=window
                )
                verify_account()
                return
    
            if status != "Active":
                messagebox.showerror(
                    "Error",
                    "Unable to verify account status.",
                    parent=window
                )
                return
    
            confirm = messagebox.askyesno(
                "Confirm Account Closure",
                f"Are you sure you want to close this account?\n\n"
                f"Customer: {name}\n"
                f"Account Number: {account_number}\n"
                f"Balance: ₹ {balance:,.2f}\n\n"
                "Transaction history will be preserved.",
                parent=window
            )
    
            if not confirm:
                return
    
            result = self.bank.close_account(account_number)
    
            if result == "closed":
                # Save Account Closure Activity
                self.bank.database.log_activity(
                    self.admin_username,
                    "Close Account",
                    f"Closed account {account_number} of customer {name}"
                )
    
                messagebox.showinfo(
                    "Account Closed",
                    f"Account closed successfully!\n\n"
                    f"Customer: {name}\n"
                    f"Account Number: {account_number}\n\n"
                    "Transaction history has been preserved.",
                    parent=window
                )
    
                verify_account()
    
            elif result == "already_closed":
    
                messagebox.showwarning(
                    "Already Closed",
                    "This account is already closed.",
                    parent=window
                )
    
                verify_account()
    
            elif result == "not_found":
    
                messagebox.showerror(
                    "Error",
                    "Account not found.",
                    parent=window
                )
    
                reset_details()
    
            elif result == "balance_remaining":
    
                messagebox.showwarning(
                    "Balance Remaining",
                    f"Account cannot be closed.\n\n"
                    f"Remaining Balance: ₹ {balance:,.2f}\n\n"
                    "Please settle the remaining balance first.",
                    parent=window
                )
    
                verify_account()
    
            else:
    
                messagebox.showerror(
                    "Error",
                    "Account closure failed.",
                    parent=window
                )
    
        tk.Button(
            form,
            text="CLOSE ACCOUNT",
            font=("Segoe UI", 11, "bold"),
            bg="#c0392b",
            fg="white",
            activebackground="#a93226",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=confirm_closure
        ).pack(fill="x", pady=(15, 3), ipady=10)
    
        account_entry.focus_set()

    def delete_account(self):

        account = simpledialog.askinteger(
            "Delete Account",
            "Enter Account Number:",
            parent=self.root
        )

        if account is None:
            return

        result = self.bank.search_account(account)

        if result is None:
            messagebox.showerror(
                "Account Not Found",
                "No account found with this account number.",
                parent=self.root
            )
            return

        account_number, name, balance = result

        # Main Window
        window = tk.Toplevel(self.root)
        window.title("SBMS - Delete Account")
        window.geometry("750x540")
        window.minsize(650, 460)
        window.configure(bg="#f1f5f9")

        # Header
        header = tk.Frame(
            window,
            bg="#142d4e",
            height=100
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="DELETE BANK ACCOUNT",
            font=("Arial", 22, "bold"),
            bg="#142d4e",
            fg="white"
        ).pack(anchor="w", padx=28, pady=(20, 4))

        tk.Label(
            header,
            text="Account Management",
            font=("Arial", 11),
            bg="#142d4e",
            fg="#cbddec"
        ).pack(anchor="w", padx=30)

        # Content
        content = tk.Frame(
            window,
            bg="#f1f5f9"
        )
        content.pack(fill="both", expand=True, padx=35, pady=25)

        # Account Details
        details_card = tk.Frame(
            content,
            bg="white",
            padx=25,
            pady=22,
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        details_card.pack(fill="x", pady=(0, 18))

        tk.Label(
            details_card,
            text="ACCOUNT INFORMATION",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w")

        details = [
            ("Customer Name", name),
            ("Account Number", str(account_number)),
            ("Current Balance", f"₹ {balance:,.2f}")
        ]

        for label_text, value_text in details:

            row = tk.Frame(
                details_card,
                bg="white"
            )
            row.pack(fill="x", pady=(12, 0))

            tk.Label(
                row,
                text=label_text,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#64748b",
                width=20,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=value_text,
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#142d4e"
            ).pack(side="left")

        # Warning Card
        warning_card = tk.Frame(
            content,
            bg="#fff7ed",
            padx=20,
            pady=16,
            highlightbackground="#fed7aa",
            highlightthickness=1
        )
        warning_card.pack(fill="x", pady=(0, 18))

        tk.Label(
            warning_card,
            text="WARNING",
            font=("Arial", 11, "bold"),
            bg="#fff7ed",
            fg="#c2410c"
        ).pack(anchor="w")

        tk.Label(
            warning_card,
            text=(
                "Account deletion is a permanent action. "
                "Accounts with transaction history cannot be deleted."
            ),
            font=("Arial", 10),
            bg="#fff7ed",
            fg="#9a3412",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(7, 0))

        # Delete Function
        def confirm_deletion():

            confirm = messagebox.askyesno(
                "Final Confirmation",
                f"Are you sure you want to delete account {account_number}?",
                parent=window
            )

            if not confirm:
                return

            delete_result = self.bank.delete_account(account_number)

            if delete_result == "deleted":
                # Save Account Deletion Activity
                self.bank.database.log_activity(
                    self.admin_username,
                    "Delete Account",
                    f"Deleted account {account_number} of customer {name}"
                )

                messagebox.showinfo(
                    "Success",
                    "Account deleted successfully!",
                    parent=window
                )

                window.destroy()

            elif delete_result == "has_transactions":

                messagebox.showwarning(
                    "Cannot Delete",
                    "This account has transaction history. "
                    "Deletion is not allowed.",
                    parent=window
                )

            elif delete_result == "not_found":

                messagebox.showerror(
                    "Error",
                    "Account not found.",
                    parent=window
                )

                window.destroy()

            else:

                messagebox.showerror(
                    "Error",
                    "Account deletion failed.",
                    parent=window
                )

        # Delete Button
        tk.Button(
            content,
            text="DELETE ACCOUNT",
            command=confirm_deletion,
            font=("Arial", 11, "bold"),
            bg="#c0392b",
            fg="white",
            activebackground="#922b21",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=12
        ).pack(anchor="center")

        # Footer
        tk.Label(
            content,
            text="SBMS  |  Secure • Reliable • Professional Banking",
            font=("Arial", 9),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(pady=(15, 0))

    def update_customer_name(self):

        account = simpledialog.askinteger(
            "Update Customer Name",
            "Enter Account Number:",
            parent=self.root
        )

        if account is None:
            return

        result = self.bank.search_account(account)

        if result is None:
            messagebox.showerror(
                "Account Not Found",
                "No account found with this account number."
            )
            return

        account_number, current_name, balance = result

        # Main Window
        window = tk.Toplevel(self.root)
        window.title("SBMS - Update Customer Name")
        window.geometry("750x530")
        window.minsize(650, 450)
        window.configure(bg="#f1f5f9")

        # Header
        header = tk.Frame(
            window,
            bg="#142d4e",
            height=100
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="UPDATE CUSTOMER NAME",
            font=("Arial", 22, "bold"),
            bg="#142d4e",
            fg="white"
        ).pack(anchor="w", padx=28, pady=(20, 4))

        tk.Label(
            header,
            text="Manage Customer Account Information",
            font=("Arial", 11),
            bg="#142d4e",
            fg="#cbddec"
        ).pack(anchor="w", padx=30)

        # Content
        content = tk.Frame(
            window,
            bg="#f1f5f9"
        )
        content.pack(fill="both", expand=True, padx=35, pady=25)

        # Account Details Card
        details_card = tk.Frame(
            content,
            bg="white",
            padx=25,
            pady=20,
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        details_card.pack(fill="x", pady=(0, 20))

        tk.Label(
            details_card,
            text="ACCOUNT INFORMATION",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w")

        tk.Label(
            details_card,
            text=f"Account Number: {account_number}",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#24577a"
        ).pack(anchor="w", pady=(12, 5))

        tk.Label(
            details_card,
            text=f"Current Customer Name: {current_name}",
            font=("Arial", 13),
            bg="white",
            fg="#142d4e"
        ).pack(anchor="w", pady=5)

        tk.Label(
            details_card,
            text=f"Current Balance: ₹ {balance:,.2f}",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#24577a"
        ).pack(anchor="w", pady=5)

        # Update Form
        form_card = tk.Frame(
            content,
            bg="white",
            padx=25,
            pady=22,
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        form_card.pack(fill="x")

        tk.Label(
            form_card,
            text="Enter New Customer Name",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(anchor="w")

        name_entry = tk.Entry(
            form_card,
            font=("Arial", 13),
            relief="solid",
            bd=1
        )
        name_entry.pack(fill="x", ipady=9, pady=(10, 18))
        name_entry.focus_set()

        # Update Function
        def save_new_name():

            new_name = name_entry.get()

            if not new_name.strip():
                messagebox.showwarning(
                    "Invalid Name",
                    "Customer name cannot be empty.",
                    parent=window
                )
                return

            update_result = self.bank.update_customer_name(
                account_number,
                new_name
            )

            if update_result == "updated":
                # Save Customer Name Update Activity
                self.bank.database.log_activity(
                    self.admin_username,
                    "Update Customer Name",
                    f"Updated account {account_number} name "
                    f"from {current_name} to {new_name.strip()}"
                )

                messagebox.showinfo(
                    "Success",
                    "Customer name updated successfully!",
                    parent=window
                )

                window.destroy()

            elif update_result == "invalid_name":

                messagebox.showwarning(
                    "Invalid Name",
                    "Customer name cannot be empty.",
                    parent=window
                )

            elif update_result == "not_found":

                messagebox.showerror(
                    "Error",
                    "Account not found.",
                    parent=window
                )

            else:

                messagebox.showerror(
                    "Error",
                    "Name update failed.",
                    parent=window
                )

        # Update Button
        tk.Button(
            form_card,
            text="UPDATE CUSTOMER NAME",
            command=save_new_name,
            font=("Arial", 11, "bold"),
            bg="#24577a",
            fg="white",
            activebackground="#142d4e",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=12
        ).pack(anchor="w")

        # Footer
        tk.Label(
            content,
            text="SBMS  |  Secure • Reliable • Professional Banking",
            font=("Arial", 9),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(pady=(15, 0))

    def display_all_accounts(self):

        accounts = self.bank.get_all_accounts()

        if accounts is None:
            messagebox.showerror(
                "Error",
                "Unable to fetch account details."
            )
            return

        if not accounts:
            messagebox.showinfo(
                "No Accounts",
                "No bank accounts found."
            )
            return

        # Main Window
        window = tk.Toplevel(self.root)
        window.title("SBMS - All Bank Accounts")
        window.geometry("1100x680")
        window.minsize(850, 500)
        window.configure(bg="#f1f5f9")

        # Header
        header = tk.Frame(
            window,
            bg="#142d4e",
            height=95
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="ALL BANK ACCOUNTS",
            font=("Arial", 22, "bold"),
            bg="#142d4e",
            fg="white"
        ).pack(anchor="w", padx=28, pady=(17, 3))

        tk.Label(
            header,
            text="Customer Account Management",
            font=("Arial", 11),
            bg="#142d4e",
            fg="#cbddec"
        ).pack(anchor="w", padx=30)

        # Main Content
        content = tk.Frame(
            window,
            bg="#f1f5f9"
        )
        content.pack(fill="both", expand=True, padx=25, pady=20)

        # Summary Card
        summary_card = tk.Frame(
            content,
            bg="white",
            padx=22,
            pady=16,
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        summary_card.pack(fill="x", pady=(0, 18))

        tk.Label(
            summary_card,
            text="TOTAL REGISTERED ACCOUNTS",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w")

        count_label = tk.Label(
            summary_card,
            text=str(len(accounts)),
            font=("Arial", 25, "bold"),
            bg="white",
            fg="#24577a"
        )
        count_label.pack(anchor="w", pady=(5, 0))

        # Search Section
        search_frame = tk.Frame(
            content,
            bg="#f1f5f9"
        )
        search_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            search_frame,
            text="Search Customer",
            font=("Arial", 11, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(anchor="w", pady=(0, 7))

        search_var = tk.StringVar()

        search_entry = tk.Entry(
            search_frame,
            textvariable=search_var,
            font=("Arial", 12),
            relief="solid",
            bd=1
        )
        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9
        )

        # Table Container
        table_frame = tk.Frame(
            content,
            bg="white",
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True)

        columns = (
            "Account Number",
            "Customer Name",
            "Balance"
        )

        # Table Style
        accounts_style = ttk.Style()

        accounts_style.configure(
            "Accounts.Treeview",
            background="white",
            foreground="#142d4e",
            rowheight=35,
            font=("Arial", 10),
            fieldbackground="white"
        )

        accounts_style.configure(
            "Accounts.Treeview.Heading",
            background="#24577a",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=10
        )

        accounts_style.map(
            "Accounts.Treeview",
            background=[("selected", "#3478b8")],
            foreground=[("selected", "white")]
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Accounts.Treeview"
        )

        tree.heading("Account Number", text="Account Number")
        tree.heading("Customer Name", text="Customer Name")
        tree.heading("Balance", text="Account Balance")

        tree.column(
            "Account Number",
            width=220,
            minwidth=150,
            anchor="center"
        )

        tree.column(
            "Customer Name",
            width=350,
            minwidth=180,
            anchor="w"
        )

        tree.column(
            "Balance",
            width=250,
            minwidth=150,
            anchor="center"
        )

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        vertical_scrollbar.pack(side="right", fill="y")
        horizontal_scrollbar.pack(side="bottom", fill="x")

        tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # Display Accounts
        def load_accounts(search_text=""):

            tree.delete(*tree.get_children())

            search_text = search_text.strip().casefold()

            filtered_accounts = [
                account for account in accounts
                if search_text in str(account[0]).casefold()
                or search_text in str(account[1]).casefold()
            ]

            for account in filtered_accounts:

                tree.insert(
                    "",
                    "end",
                    values=(
                        account[0],
                        account[1],
                        f"₹ {account[2]:,.2f}"
                    )
                )

            count_label.config(
                text=f"{len(filtered_accounts)} / {len(accounts)}"
            )

        # Live Search
        def filter_accounts(*args):
            load_accounts(search_var.get())

        search_var.trace_add("write", filter_accounts)

        # Initial Data
        load_accounts()

        # Footer
        tk.Label(
            content,
            text="SBMS  |  Secure • Reliable • Professional Banking",
            font=("Arial", 9),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(pady=(12, 0))

    def search_account(self):

        account = simpledialog.askinteger(
            "Search Account",
            "Enter Account Number:",
            parent=self.root
        )

        if account is None:
            return

        result = self.bank.search_account(account)

        if result is None:
            messagebox.showerror(
                "Account Not Found",
                "No account found with this account number."
            )
            return

        account_number, name, balance = result
        status = self.bank.get_account_status(account_number)

        # Main Window
        window = tk.Toplevel(self.root)
        window.title("SBMS - Customer Profile")
        window.geometry("750x520")
        window.minsize(650, 450)
        window.configure(bg="#f1f5f9")

        # Header
        header = tk.Frame(
            window,
            bg="#142d4e",
            height=100
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="CUSTOMER PROFILE",
            font=("Arial", 22, "bold"),
            bg="#142d4e",
            fg="white"
        ).pack(anchor="w", padx=28, pady=(20, 4))

        tk.Label(
            header,
            text="Customer Account Information",
            font=("Arial", 11),
            bg="#142d4e",
            fg="#cbddec"
        ).pack(anchor="w", padx=30)

        # Content
        content = tk.Frame(
            window,
            bg="#f1f5f9"
        )
        content.pack(fill="both", expand=True, padx=35, pady=28)

        # Profile Card
        profile_card = tk.Frame(
            content,
            bg="white",
            highlightbackground="#dbe4ee",
            highlightthickness=1,
            padx=25,
            pady=25
        )
        profile_card.pack(fill="x", pady=(0, 20))

        tk.Label(
            profile_card,
            text="CUSTOMER NAME",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#64748b"
        ).pack(anchor="w")

        tk.Label(
            profile_card,
            text=name,
            font=("Arial", 23, "bold"),
            bg="white",
            fg="#142d4e"
        ).pack(anchor="w", pady=(7, 18))

        tk.Frame(
            profile_card,
            bg="#e2e8f0",
            height=1
        ).pack(fill="x", pady=(0, 18))

        # Account Information
        details_frame = tk.Frame(
            profile_card,
            bg="white"
        )
        details_frame.pack(fill="x")

        tk.Label(
            details_frame,
            text="ACCOUNT NUMBER",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#64748b"
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            details_frame,
            text=str(account_number),
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#24577a"
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))
        tk.Label(
            details_frame,
            text="ACCOUNT STATUS",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#64748b"
        ).grid(row=0, column=1, sticky="w", padx=(60, 0))

        status_color = "#16a34a" if status == "Active" else "#dc2626"

        tk.Label(
            details_frame,
            text=status,
            font=("Arial", 13, "bold"),
            bg="white",
            fg=status_color
        ).grid(row=1, column=1, sticky="w", padx=(60, 0))

        # Balance Card
        balance_card = tk.Frame(
            content,
            bg="#24577a",
            padx=25,
            pady=22
        )
        balance_card.pack(fill="x")

        tk.Label(
            balance_card,
            text="CURRENT ACCOUNT BALANCE",
            font=("Arial", 10, "bold"),
            bg="#24577a",
            fg="#dbeafe"
        ).pack(anchor="w")

        tk.Label(
            balance_card,
            text=f"₹ {balance:,.2f}",
            font=("Arial", 25, "bold"),
            bg="#24577a",
            fg="white"
        ).pack(anchor="w", pady=(8, 0))

        # Footer
        tk.Label(
            content,
            text="SBMS  |  Secure • Reliable • Professional Banking",
            font=("Arial", 9),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(pady=(20, 0))

    def account_statement(self):

        account = simpledialog.askinteger(
            "Account Statement",
            "Enter Account Number:",
            parent=self.root
        )

        if account is None:
            return

        statement = self.bank.get_account_statement(account)

        if statement is None:
            messagebox.showerror(
                "Error",
                "Unable to fetch account statement."
            )
            return

        if not statement:
            messagebox.showinfo(
                "No Transactions",
                "No transaction history found for this account."
            )
            return

        summary = self.bank.get_account_summary(account)

        if summary is None:
            messagebox.showerror(
                "Error",
                "Unable to fetch account summary."
            )
            return

        name, balance, deposits, withdrawals, total_txns = summary

        # Main Window
        window = tk.Toplevel(self.root)
        window.title("SBMS - Account Statement")
        window.geometry("1100x680")
        window.minsize(900, 550)
        window.configure(bg="#f1f5f9")

        # Header
        header = tk.Frame(
            window,
            bg="#142d4e",
            height=90
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="ACCOUNT STATEMENT",
            font=("Arial", 22, "bold"),
            bg="#142d4e",
            fg="white"
        ).pack(anchor="w", padx=25, pady=(15, 3))

        tk.Label(
            header,
            text=f"Customer: {name}  |  Account Number: {account}",
            font=("Arial", 11),
            bg="#142d4e",
            fg="#cbddec"
        ).pack(anchor="w", padx=27)

        # Main Content
        content = tk.Frame(
            window,
            bg="#f1f5f9"
        )
        content.pack(fill="both", expand=True, padx=22, pady=18)

        # Summary Heading
        tk.Label(
            content,
            text="Account Overview",
            font=("Arial", 17, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(anchor="w", pady=(0, 12))

        # Summary Cards
        summary_frame = tk.Frame(
            content,
            bg="#f1f5f9"
        )
        summary_frame.pack(fill="x", pady=(0, 22))

        cards = [
            ("Current Balance", f"₹ {balance:,.2f}"),
            ("Total Deposits", f"₹ {deposits:,.2f}"),
            ("Total Withdrawals", f"₹ {withdrawals:,.2f}"),
            ("Total Transactions", str(total_txns))
        ]

        for index, (title, value) in enumerate(cards):

            card = tk.Frame(
                summary_frame,
                bg="white",
                padx=15,
                pady=18,
                highlightbackground="#dbe4ee",
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index,
                padx=6,
                pady=5,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=title,
                font=("Arial", 9, "bold"),
                bg="white",
                fg="#64748b"
            ).pack(anchor="w")

            tk.Label(
                card,
                text=value,
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#24577a"
            ).pack(anchor="w", pady=(10, 0))

            summary_frame.grid_columnconfigure(
                index,
                weight=1
            )

        # Transaction History Heading
        tk.Label(
            content,
            text="Transaction History",
            font=("Arial", 17, "bold"),
            bg="#f1f5f9",
            fg="#142d4e"
        ).pack(anchor="w", pady=(0, 12))

        # Table Container
        table_frame = tk.Frame(
            content,
            bg="white",
            highlightbackground="#dbe4ee",
            highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True)

        columns = (
            "Transaction ID",
            "Type",
            "Amount",
            "Date & Time",
            "Receiver"
        )

        # Custom Table Style
        statement_style = ttk.Style()

        statement_style.configure(
            "Statement.Treeview",
            background="white",
            foreground="#142d4e",
            rowheight=32,
            font=("Arial", 10),
            fieldbackground="white"
        )
        statement_style.configure(
            "Statement.Treeview.Heading",
            background="#24577a",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=9
        )
        statement_style.map(
            "Statement.Treeview",
            background=[("selected", "#3478b8")],
            foreground=[("selected", "white")]
        )
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Statement.Treeview"
        )
        column_widths = {
            "Transaction ID": 150,
            "Type": 160,
            "Amount": 150,
            "Date & Time": 220,
            "Receiver": 150
        }
        for column in columns:
            tree.heading(
                column,
                text=column
            )
            tree.column(
                column,
                width=column_widths[column],
                minwidth=100,
                anchor="center"
            )
        # Insert Transactions
        for transaction in statement:
            txn_id, txn_type, amount, timestamp, receiver = transaction
            tree.insert(
                "",
                "end",
                values=(
                    txn_id,
                    txn_type,
                    f"₹ {amount:,.2f}",
                    timestamp,
                    receiver if receiver is not None else "-"
                )
            )
        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )
        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=tree.xview
        )
        tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )
        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )
        horizontal_scrollbar.pack(
            side="bottom",
            fill="x"
        )
        tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )
        # Footer
        tk.Label(
            content,
            text="SBMS  |  Secure • Reliable • Professional Banking",
            font=("Arial", 9),
            bg="#f1f5f9",
            fg="#64748b"
        ).pack(pady=(12, 0))