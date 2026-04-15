import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, on_show_signup=None):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.on_show_signup = on_show_signup

        # Configure main frame
        self.configure(fg_color="#0a0a0a")

        # Create main container with gradient-like effect
        self.main_container = ctk.CTkFrame(
            self,
            fg_color="#1a1a1a",
            border_width=2,
            border_color="#2a2a2a",
            corner_radius=20,
            width=450,
            height=550
        )
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome section
        self.create_welcome_section()

        # Login form
        self.create_login_form()

        # Footer
        self.create_footer()

    def create_welcome_section(self):
        """Create the welcome header section"""
        # App title with icon-like styling
        self.title_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.title_frame.pack(pady=(40, 20))

        # App icon (using text as icon)
        self.icon_label = ctk.CTkLabel(
            self.title_frame,
            text="🔐",
            font=ctk.CTkFont(size=48)
        )
        self.icon_label.pack()

        # Main title
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Welcome Back",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=(10, 5))

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Sign in to your account",
            font=ctk.CTkFont(size=14),
            text_color="#a0a0a0"
        )
        self.subtitle_label.pack()

    def create_login_form(self):
        """Create the login form section"""
        # Form container
        self.form_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.form_frame.pack(pady=(20, 30), padx=40)

        # Username field with icon
        self.username_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="#2a2a2a",
            corner_radius=10,
            border_width=1,
            border_color="#404040"
        )
        self.username_frame.pack(fill="x", pady=(0, 15))

        self.username_icon = ctk.CTkLabel(
            self.username_frame,
            text="👤",
            font=ctk.CTkFont(size=16)
        )
        self.username_icon.pack(side="left", padx=(15, 5))

        self.username_entry = ctk.CTkEntry(
            self.username_frame,
            placeholder_text="Enter your username",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            width=300
        )
        self.username_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=10)

        # Password field with icon
        self.password_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="#2a2a2a",
            corner_radius=10,
            border_width=1,
            border_color="#404040"
        )
        self.password_frame.pack(fill="x", pady=(0, 25))

        self.password_icon = ctk.CTkLabel(
            self.password_frame,
            text="🔒",
            font=ctk.CTkFont(size=16)
        )
        self.password_icon.pack(side="left", padx=(15, 5))

        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Enter your password",
            show="•",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            width=300
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=10)

        # Login button with gradient effect
        self.login_btn = ctk.CTkButton(
            self.form_frame,
            text="Sign In",
            command=self.login,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#007acc",
            hover_color="#005999"
        )
        self.login_btn.pack(fill="x", pady=(10, 0))

        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())

    def create_footer(self):
        """Create the footer section with signup link"""
        if self.on_show_signup:
            self.footer_frame = ctk.CTkFrame(
                self.main_container,
                fg_color="transparent"
            )
            self.footer_frame.pack(pady=(20, 40))

            # Separator line
            self.separator = ctk.CTkFrame(
                self.footer_frame,
                height=1,
                fg_color="#404040"
            )
            self.separator.pack(fill="x", pady=(0, 20))

            # Signup section
            self.signup_text = ctk.CTkLabel(
                self.footer_frame,
                text="New to Smart Management?",
                font=ctk.CTkFont(size=14),
                text_color="#a0a0a0"
            )
            self.signup_text.pack()

            self.signup_btn = ctk.CTkButton(
                self.footer_frame,
                text="Create Account",
                command=self.on_show_signup,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="transparent",
                hover_color="#2a2a2a",
                border_width=2,
                border_color="#007acc",
                corner_radius=8
            )
            self.signup_btn.pack(pady=(10, 0))

    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror(
                "Login Failed",
                "Please enter both username and password",
                parent=self.winfo_toplevel()
            )
            return

        # Add loading state
        self.login_btn.configure(text="Signing In...", state="disabled")
        self.update()

        try:
            # This will be handled by the main app with controller
            self.on_login_success(username, password)
        except Exception as e:
            messagebox.showerror(
                "Login Error",
                f"An error occurred: {str(e)}",
                parent=self.winfo_toplevel()
            )
        finally:
            # Reset button state
            self.login_btn.configure(text="Sign In", state="normal")
