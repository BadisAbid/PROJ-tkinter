import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, callback):
        super().__init__(parent, width=200, corner_radius=0)
        self.callback = callback

        self.logo_label = ctk.CTkLabel(self, text="Smart System", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.dashboard_btn = ctk.CTkButton(self, text="Dashboard", command=lambda: self.callback("Dashboard"))
        self.dashboard_btn.grid(row=1, column=0, padx=20, pady=10)

        self.categories_btn = ctk.CTkButton(self, text="Categories", command=lambda: self.callback("Categories"))
        self.categories_btn.grid(row=2, column=0, padx=20, pady=10)

        self.products_btn = ctk.CTkButton(self, text="Products", command=lambda: self.callback("Products"))
        self.products_btn.grid(row=3, column=0, padx=20, pady=10)

        self.orders_btn = ctk.CTkButton(self, text="Orders", command=lambda: self.callback("Orders"))
        self.orders_btn.grid(row=4, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(40, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("Dark")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
