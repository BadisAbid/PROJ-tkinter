import customtkinter as ctk

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Dashboard Overview", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        # Stats Container
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(fill="x", padx=40, pady=20)

        self.refresh_stats()

    def refresh_stats(self):
        stats = self.controller.get_dashboard_stats()

        # Clear old stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Create Stat Cards
        cards = [
            ("Total Products", stats['total_products']),
            ("Total Stock", stats['total_stock']),
            ("Total Orders", stats['total_orders']),
            ("Total Revenue", f"${stats['total_revenue']:.2f}")
        ]

        for i, (title, value) in enumerate(cards):
            card = ctk.CTkFrame(self.stats_frame, width=200, height=100, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10)
            card.grid_propagate(False)

            ctk.CTkLabel(card, text=title, font=("Arial", 12)).pack(pady=(10, 5))
            ctk.CTkLabel(card, text=str(value), font=("Arial", 18, "bold")).pack()
