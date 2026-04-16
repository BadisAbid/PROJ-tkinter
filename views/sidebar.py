
import customtkinter as ctk

# =============================================
#  SIDEBAR
#  Navigation menu on the left side.
#  Shows buttons for each page + logout.
# =============================================

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, on_page_change, on_logout):
        super().__init__(parent, width=210, corner_radius=0, fg_color="#12122a")

        # Store callbacks
        self.on_page_change = on_page_change
        self.on_logout = on_logout
        self.current_page = None  # Track which page is selected

        # Prevent the sidebar from shrinking
        self.pack_propagate(False)

        self._build_sidebar()

    # --------------------------------------------------
    def _build_sidebar(self):
        """Create all sidebar widgets."""

        # --- LOGO / APP NAME ---
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(25, 5), padx=15)

        ctk.CTkLabel(
            logo_frame,
            text="🛒",
            font=ctk.CTkFont(size=32),
        ).pack(side="left")

        ctk.CTkLabel(
            logo_frame,
            text="ShopManager",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#7c83fd",
        ).pack(side="left", padx=(8, 0))

        # Divider line
        ctk.CTkFrame(self, height=1, fg_color="#2a2a4a").pack(
            fill="x", padx=15, pady=(10, 20)
        )

        # --- NAVIGATION LABEL ---
        ctk.CTkLabel(
            self,
            text="NAVIGATION",
            font=ctk.CTkFont(size=10),
            text_color="#555570",
            anchor="w",
        ).pack(fill="x", padx=20, pady=(0, 8))

        # --- NAV BUTTONS ---
        # Each tuple: (emoji, label, page_name)
        nav_items = [
            ("📊", "Dashboard",  "Dashboard"),
            ("📂", "Categories", "Categories"),
            ("📦", "Products",   "Products"),
            ("🛒", "Orders",     "Orders"),
        ]

        self.nav_buttons = {}  # Store buttons so we can highlight active one

        for icon, label, page in nav_items:
            btn = ctk.CTkButton(
                self,
                text=f"  {icon}  {label}",
                anchor="w",
                height=42,
                corner_radius=10,
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color="#2a2a4a",
                text_color="#bbbbcc",
                command=lambda p=page: self._navigate(p),
            )
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[page] = btn

        # --- APPEARANCE TOGGLE ---
        ctk.CTkFrame(self, height=1, fg_color="#2a2a4a").pack(
            fill="x", padx=15, pady=(20, 15)
        )

        ctk.CTkLabel(
            self,
            text="APPEARANCE",
            font=ctk.CTkFont(size=10),
            text_color="#555570",
            anchor="w",
        ).pack(fill="x", padx=20, pady=(0, 6))

        self.mode_menu = ctk.CTkOptionMenu(
            self,
            values=["Dark", "Light", "System"],
            command=self._change_appearance,
            fg_color="#1e1e3e",
            button_color="#7c83fd",
            button_hover_color="#5a60d0",
            font=ctk.CTkFont(size=13),
            height=36,
            corner_radius=8,
        )
        self.mode_menu.set("Dark")
        self.mode_menu.pack(fill="x", padx=12)

        # --- LOGOUT BUTTON (pushed to bottom) ---
        self.logout_btn = ctk.CTkButton(
            self,
            text="  🚪  Logout",
            anchor="w",
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            hover_color="#3a1a1a",
            text_color="#e05555",
            command=self.on_logout,
        )
        self.logout_btn.pack(fill="x", padx=12, pady=(20, 20), side="bottom")

    # --------------------------------------------------
    def _navigate(self, page_name):
        """Highlight the selected button and call the page callback."""
        # Reset all buttons to default style
        for name, btn in self.nav_buttons.items():
            btn.configure(fg_color="transparent", text_color="#bbbbcc")

        # Highlight the active button
        if page_name in self.nav_buttons:
            self.nav_buttons[page_name].configure(
                fg_color="#2a2a4a", text_color="#7c83fd"
            )

        self.current_page = page_name
        self.on_page_change(page_name)

    # --------------------------------------------------
    def highlight(self, page_name):
        """Manually highlight a page button (called from outside)."""
        self._navigate(page_name)

    # --------------------------------------------------
    def _change_appearance(self, mode):
        ctk.set_appearance_mode(mode)
