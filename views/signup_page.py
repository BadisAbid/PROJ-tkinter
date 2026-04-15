import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk

class SignupPage(ctk.CTkFrame):
    def __init__(self, parent, on_signup_success, on_back_to_login):
        super().__init__(parent)
        self.on_signup_success = on_signup_success
        self.on_back_to_login = on_back_to_login

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
            height=650  # Increased height for email field
        )
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome section
        self.create_welcome_section()

        # Signup form
        self.create_signup_form()

        # Footer
        self.create_footer()

    def create_welcome_section(self):
        """Create the welcome header section"""
        # App title with icon-like styling
        self.title_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.title_frame.pack(pady=(30, 15))

        # Signup icon
        self.icon_label = ctk.CTkLabel(
            self.title_frame,
            text="📝",
            font=ctk.CTkFont(size=48)
        )
        self.icon_label.pack()

        # Main title
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Create Account",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=(10, 5))

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Join Smart Management System",
            font=ctk.CTkFont(size=14),
            text_color="#a0a0a0"
        )
        self.subtitle_label.pack()

    def create_signup_form(self):
        """Create the signup form section"""
        # Form container
        self.form_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.form_frame.pack(pady=(15, 25), padx=40)

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
            placeholder_text="Choose a username",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            width=300
        )
        self.username_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=10)

        # Email field with icon
        self.email_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="#2a2a2a",
            corner_radius=10,
            border_width=1,
            border_color="#404040"
        )
        self.email_frame.pack(fill="x", pady=(0, 15))

        self.email_icon = ctk.CTkLabel(
            self.email_frame,
            text="📧",
            font=ctk.CTkFont(size=16)
        )
        self.email_icon.pack(side="left", padx=(15, 5))

        self.email_entry = ctk.CTkEntry(
            self.email_frame,
            placeholder_text="Enter your email address",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            width=300
        )
        self.email_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=10)

        # Password field with icon
        self.password_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="#2a2a2a",
            corner_radius=10,
            border_width=1,
            border_color="#404040"
        )
        self.password_frame.pack(fill="x", pady=(0, 15))

        self.password_icon = ctk.CTkLabel(
            self.password_frame,
            text="🔒",
            font=ctk.CTkFont(size=16)
        )
        self.password_icon.pack(side="left", padx=(15, 5))

        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Create a password",
            show="•",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            width=300
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=10)

        # Confirm password field with icon
        self.confirm_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="#2a2a2a",
            corner_radius=10,
            border_width=1,
            border_color="#404040"
        )
        self.confirm_frame.pack(fill="x", pady=(0, 25))

        self.confirm_icon = ctk.CTkLabel(
            self.confirm_frame,
            text="🔐",
            font=ctk.CTkFont(size=16)
        )
        self.confirm_icon.pack(side="left", padx=(15, 5))

        self.confirm_password_entry = ctk.CTkEntry(
            self.confirm_frame,
            placeholder_text="Confirm your password",
            show="•",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=0,
            width=300
        )
        self.confirm_password_entry.pack(side="left", fill="x", expand=True, padx=(0, 15), pady=10)

        # Password strength indicator
        self.strength_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )
        self.strength_frame.pack(fill="x", pady=(0, 10))

        self.strength_label = ctk.CTkLabel(
            self.strength_frame,
            text="Password Strength: ",
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0"
        )
        self.strength_label.pack(side="left")

        self.strength_indicator = ctk.CTkLabel(
            self.strength_frame,
            text="Weak",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#dc3545"
        )
        self.strength_indicator.pack(side="left")

        # Password requirements
        self.requirements_label = ctk.CTkLabel(
            self.form_frame,
            text="Requirements: 8+ chars, uppercase, lowercase, number, special char",
            font=ctk.CTkFont(size=10),
            text_color="#808080",
            wraplength=400
        )
        self.requirements_label.pack(pady=(0, 15), anchor="w")

        # Bind password entry to update strength
        self.password_entry.bind("<KeyRelease>", self.update_password_strength)

        # Terms checkbox
        self.terms_var = ctk.BooleanVar()
        self.terms_checkbox = ctk.CTkCheckBox(
            self.form_frame,
            text="I agree to the Terms of Service and Privacy Policy",
            variable=self.terms_var,
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0",
            fg_color="#007acc",
            hover_color="#005999"
        )
        self.terms_checkbox.pack(pady=(0, 20), anchor="w")

        # Signup button with gradient effect
        self.signup_btn = ctk.CTkButton(
            self.form_frame,
            text="Create Account",
            command=self.signup,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            corner_radius=10,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.signup_btn.pack(fill="x", pady=(10, 0))

        # Bind Enter key to signup
        self.confirm_password_entry.bind("<Return>", lambda e: self.signup())

    def create_footer(self):
        """Create the footer section with back to login"""
        self.footer_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.footer_frame.pack(pady=(15, 30))

        # Separator line
        self.separator = ctk.CTkFrame(
            self.footer_frame,
            height=1,
            fg_color="#404040"
        )
        self.separator.pack(fill="x", pady=(0, 20))

        # Back to login section
        self.login_text = ctk.CTkLabel(
            self.footer_frame,
            text="Already have an account?",
            font=ctk.CTkFont(size=14),
            text_color="#a0a0a0"
        )
        self.login_text.pack()

        self.back_btn = ctk.CTkButton(
            self.footer_frame,
            text="Sign In",
            command=self.on_back_to_login,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            hover_color="#2a2a2a",
            border_width=2,
            border_color="#007acc",
            corner_radius=8
        )
        self.back_btn.pack(pady=(10, 0))

    def validate_email(self, email):
        """Validate email format using regex"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_password_complexity(self, password):
        """Validate password meets complexity requirements"""
        import re

        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"

        return True, "Password meets all requirements"

    def update_password_strength(self, event=None):
        """Update password strength indicator with detailed requirements"""
        import re

        password = self.password_entry.get()

        if len(password) == 0:
            self.strength_indicator.configure(text="None", text_color="#a0a0a0")
            return

        # Check requirements
        has_length = len(password) >= 8
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_number = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

        requirements_met = sum([has_length, has_uppercase, has_lowercase, has_number, has_special])

        if requirements_met <= 2:
            self.strength_indicator.configure(text="Weak", text_color="#dc3545")
        elif requirements_met <= 3:
            self.strength_indicator.configure(text="Fair", text_color="#ffc107")
        elif requirements_met <= 4:
            self.strength_indicator.configure(text="Good", text_color="#28a745")
        else:
            self.strength_indicator.configure(text="Strong", text_color="#007acc")

    def signup(self):
        """Handle signup attempt"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validation
        if not username:
            messagebox.showerror(
                "Validation Error",
                "Please enter a username",
                parent=self.winfo_toplevel()
            )
            self.username_entry.focus()
            return

        if not email:
            messagebox.showerror(
                "Validation Error",
                "Please enter an email address",
                parent=self.winfo_toplevel()
            )
            self.email_entry.focus()
            return

        if not self.validate_email(email):
            messagebox.showerror(
                "Validation Error",
                "Please enter a valid email address",
                parent=self.winfo_toplevel()
            )
            self.email_entry.focus()
            return

        if not password:
            messagebox.showerror(
                "Validation Error",
                "Please enter a password",
                parent=self.winfo_toplevel()
            )
            self.password_entry.focus()
            return

        if not confirm_password:
            messagebox.showerror(
                "Validation Error",
                "Please confirm your password",
                parent=self.winfo_toplevel()
            )
            self.confirm_password_entry.focus()
            return

        if password != confirm_password:
            messagebox.showerror(
                "Validation Error",
                "Passwords do not match",
                parent=self.winfo_toplevel()
            )
            self.confirm_password_entry.focus()
            return

        # Enhanced password validation
        is_valid_password, password_error = self.validate_password_complexity(password)
        if not is_valid_password:
            messagebox.showerror(
                "Password Requirements",
                password_error,
                parent=self.winfo_toplevel()
            )
            self.password_entry.focus()
            return

        if not self.terms_var.get():
            messagebox.showerror(
                "Terms Required",
                "Please agree to the Terms of Service and Privacy Policy",
                parent=self.winfo_toplevel()
            )
            return

        # Add loading state
        self.signup_btn.configure(text="Creating Account...", state="disabled")
        self.update()

        try:
            # Call the signup callback (will be handled by main app)
            self.on_signup_success(username, email, password)
        except Exception as e:
            messagebox.showerror(
                "Signup Error",
                f"An error occurred: {str(e)}",
                parent=self.winfo_toplevel()
            )
        finally:
            # Reset button state
            self.signup_btn.configure(text="Create Account", state="normal")