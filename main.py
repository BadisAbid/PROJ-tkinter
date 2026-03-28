import customtkinter as ctk
from tkinter import messagebox
from controllers.main_controller import MainController
from views.sidebar import Sidebar
from views.dashboard_page import DashboardPage
from views.category_page import CategoryPage
from views.product_page import ProductPage
from views.order_page import OrderPage
from views.login_page import LoginPage

class SmartManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Management System")
        self.geometry("1100x600")
        
        # Set appearance
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Initialize Controller
        self.controller = MainController()

        # Auth State
        self.is_authenticated = False

        # Main Content Area
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)

        self.show_login()

    def show_login(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        login = LoginPage(self.main_container, self.on_login_success)
        login.pack(fill="both", expand=True)

    def on_login_success(self):
        self.is_authenticated = True
        self.setup_main_ui()

    def setup_main_ui(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

        # Layout
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self.main_container, self.show_page)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Page Area
        self.page_frame = ctk.CTkFrame(self.main_container)
        self.page_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.page_frame.grid_columnconfigure(0, weight=1)
        self.page_frame.grid_rowconfigure(0, weight=1)

        self.show_page("Dashboard")

    def show_page(self, page_name):
        # Clean current page
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        if page_name == "Dashboard":
            page = DashboardPage(self.page_frame, self.controller)
        elif page_name == "Categories":
            page = CategoryPage(self.page_frame, self.controller)
        elif page_name == "Products":
            page = ProductPage(self.page_frame, self.controller)
        elif page_name == "Orders":
            page = OrderPage(self.page_frame, self.controller)
        else:
            page = ctk.CTkLabel(self.page_frame, text=f"{page_name} Coming Soon...", font=("Arial", 24))
        
        page.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = SmartManagementApp()
    app.mainloop()
