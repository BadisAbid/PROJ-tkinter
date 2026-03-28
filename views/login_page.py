import customtkinter as ctk
from tkinter import messagebox

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success

        # Center Frame
        self.login_frame = ctk.CTkFrame(self, width=300, height=400)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = ctk.CTkLabel(self.login_frame, text="System Login", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(40, 30))

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=220)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=220)
        self.password_entry.pack(pady=10)

        self.login_btn = ctk.CTkButton(self.login_frame, text="Login", command=self.login, width=220)
        self.login_btn.pack(pady=(30, 40))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simple check (In a real app, query the database)
        if username == "admin" and password == "admin123":
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
