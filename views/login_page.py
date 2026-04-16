
import customtkinter as ctk
from tkinter import messagebox

# =============================================
#  LOGIN PAGE
#  A small, centered login card.
#  The whole app window expands once the user
#  clicks "Sign In" and logs in successfully.
# =============================================

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, on_show_signup=None):
        super().__init__(parent)

        # Store the callback functions
        self.on_login_success = on_login_success
        self.on_show_signup = on_show_signup

        # Dark background for the whole page
        self.configure(fg_color="#0d0d1a")

        # ---------- LOGIN CARD ----------
        self.card = ctk.CTkFrame(
            self,
            fg_color="#1a1a2e",
            border_width=1,
            border_color="#3a3a6e",
            corner_radius=20,
            width=400,
            height=520,
        )
        # Place card in the center of the screen
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        # Prevent the card from shrinking to fit widgets
        self.card.pack_propagate(False)

        self._build_card()

    # --------------------------------------------------
    def _build_card(self):
        """Build everything inside the login card."""

        # --- APP ICON / LOGO ---
        ctk.CTkLabel(
            self.card,
            text="🛒",
            font=ctk.CTkFont(size=52),
        ).pack(pady=(35, 0))

        ctk.CTkLabel(
            self.card,
            text="ShopManager",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#7c83fd",
        ).pack(pady=(6, 2))

        ctk.CTkLabel(
            self.card,
            text="Sign in to continue",
            font=ctk.CTkFont(size=13),
            text_color="#888899",
        ).pack(pady=(0, 20))

        # --- ROLE SWITCH ---
        self.role_var = ctk.StringVar(value="Client")
        self.role_switch = ctk.CTkSegmentedButton(
            self.card,
            values=["Client", "Admin"],
            variable=self.role_var,
            selected_color="#7c83fd",
            unselected_color="#252540",
            selected_hover_color="#5a60d0",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=32,
        )
        self.role_switch.pack(pady=(0, 20))

        # --- USERNAME FIELD ---
        ctk.CTkLabel(
            self.card,
            text="Username",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ccccdd",
            anchor="w",
        ).pack(fill="x", padx=40)

        self.username_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Enter your username",
            height=42,
            corner_radius=10,
            border_color="#3a3a6e",
            fg_color="#252540",
            text_color="#ffffff",
            font=ctk.CTkFont(size=13),
        )
        self.username_entry.pack(fill="x", padx=40, pady=(4, 14))

        # --- PASSWORD FIELD ---
        ctk.CTkLabel(
            self.card,
            text="Password",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ccccdd",
            anchor="w",
        ).pack(fill="x", padx=40)

        self.password_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Enter your password",
            show="●",
            height=42,
            corner_radius=10,
            border_color="#3a3a6e",
            fg_color="#252540",
            text_color="#ffffff",
            font=ctk.CTkFont(size=13),
        )
        self.password_entry.pack(fill="x", padx=40, pady=(4, 22))

        # --- SIGN IN BUTTON ---
        self.login_btn = ctk.CTkButton(
            self.card,
            text="Sign In  →",
            height=44,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#7c83fd",
            hover_color="#5a60d0",
            command=self._do_login,
        )
        self.login_btn.pack(fill="x", padx=40)

        # --- DIVIDER ---
        ctk.CTkFrame(self.card, height=1, fg_color="#3a3a6e").pack(
            fill="x", padx=40, pady=(22, 16)
        )

        # --- SIGNUP LINK ---
        self.signup_row = ctk.CTkFrame(self.card, fg_color="transparent")
        self.signup_row.pack()

        ctk.CTkLabel(
            self.signup_row,
            text="No account yet?",
            font=ctk.CTkFont(size=13),
            text_color="#888899",
        ).pack(side="left")

        ctk.CTkButton(
            self.signup_row,
            text="Create one",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="transparent",
            hover_color="#252540",
            text_color="#7c83fd",
            width=80,
            command=self.on_show_signup,
        ).pack(side="left")

        # Hide signup row if "Admin" is selected
        def _toggle_signup_vis(*args):
            if self.role_var.get() == "Admin":
                self.signup_row.pack_forget()
            else:
                self.signup_row.pack()

        self.role_var.trace_add("write", _toggle_signup_vis)

        # Allow pressing Enter to login
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._do_login())

    # --------------------------------------------------
    def _do_login(self):
        """Collect username/password and call the login callback."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Basic validation
        if not username or not password:
            messagebox.showerror(
                "Missing Info",
                "Please enter both username and password.",
                parent=self.winfo_toplevel(),
            )
            return

        # Show loading state
        self.login_btn.configure(text="Signing in…", state="disabled")
        self.update()

        try:
            selected_role = self.role_var.get().lower()
            self.on_login_success(username, password, selected_role)
        except Exception as err:
            messagebox.showerror(
                "Login Error",
                f"Something went wrong:\n{err}",
                parent=self.winfo_toplevel(),
            )
        finally:
            # Reset button
            self.login_btn.configure(text="Sign In  →", state="normal")
