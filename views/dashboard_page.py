import customtkinter as ctk
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Use non-interactive backend
matplotlib.use('TkAgg')

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure main frame
        self.configure(fg_color="#0a0a0a")

        # Create scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#0a0a0a",
            label_text="Dashboard",
            label_font=ctk.CTkFont(size=20, weight="bold")
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create dashboard sections
        self.create_header_section()
        self.create_welcome_section()
        self.create_stats_section()
        self.create_graphs_section()
        self.create_quick_actions_section()

        # Initial data load
        self.refresh_stats()

    def create_header_section(self):
        """Create the header section with logo and navigation"""
        # Header frame
        self.header_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent",
            height=60
        )
        self.header_frame.pack(fill="x", padx=10, pady=(10, 0))
        self.header_frame.pack_propagate(False)

        # Dashboard icon and title
        self.icon_label = ctk.CTkLabel(
            self.header_frame,
            text="📊",
            font=ctk.CTkFont(size=32)
        )
        self.icon_label.pack(side="left")

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(side="left", padx=(15, 0))

        # Current date/time
        self.datetime_label = ctk.CTkLabel(
            self.header_frame,
            text=datetime.now().strftime("%B %d, %Y • %I:%M %p"),
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0"
        )
        self.datetime_label.pack(side="right")

        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            self.header_frame,
            text="🔄",
            width=40,
            height=40,
            corner_radius=8,
            fg_color="#2a2a2a",
            hover_color="#404040",
            command=self.refresh_stats
        )
        self.refresh_btn.pack(side="right", padx=(10, 0))

    def create_welcome_section(self):
        """Create the welcome message section"""
        # Welcome frame
        self.welcome_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent"
        )
        self.welcome_frame.pack(fill="x", padx=10, pady=(5, 10))

        # Welcome message
        self.welcome_label = ctk.CTkLabel(
            self.welcome_frame,
            text="Welcome back! Here's your business overview.",
            font=ctk.CTkFont(size=16),
            text_color="#a0a0a0"
        )
        self.welcome_label.pack(anchor="w")

    def create_stats_section(self):
        """Create the statistics cards section"""
        # Stats container
        self.stats_container = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent"
        )
        self.stats_container.pack(fill="x", padx=10, pady=(0, 15))

        # Section title
        self.stats_title = ctk.CTkLabel(
            self.stats_container,
            text="Business Statistics",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        self.stats_title.pack(anchor="w", pady=(0, 15))

        # Stats grid frame
        self.stats_frame = ctk.CTkFrame(
            self.stats_container,
            fg_color="transparent"
        )
        self.stats_frame.pack(fill="x")

    def create_graphs_section(self):
        """Create the graphs section for products and categories"""
        # Graphs container
        self.graphs_container = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent"
        )
        self.graphs_container.pack(fill="both", expand=True, padx=10, pady=(0, 15))

        # Section title
        self.graphs_title = ctk.CTkLabel(
            self.graphs_container,
            text="Analytics & Insights",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        self.graphs_title.pack(anchor="w", pady=(0, 15))

        # Graphs grid frame
        self.graphs_frame = ctk.CTkFrame(
            self.graphs_container,
            fg_color="transparent"
        )
        self.graphs_frame.pack(fill="both", expand=True)

    def create_quick_actions_section(self):
        """Create the quick actions section"""
        # Actions container
        self.actions_container = ctk.CTkFrame(
            self.scroll_frame,
            fg_color="transparent"
        )
        self.actions_container.pack(fill="x", padx=10, pady=(0, 20))

        # Section title
        self.actions_title = ctk.CTkLabel(
            self.actions_container,
            text="Quick Actions",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        self.actions_title.pack(anchor="w", pady=(0, 15))

        # Actions grid
        self.actions_frame = ctk.CTkFrame(
            self.actions_container,
            fg_color="transparent"
        )
        self.actions_frame.pack(fill="x")

        # Action buttons - removed Counter
        actions = [
            ("📦", "Manage Products", "Products"),
            ("📂", "Manage Categories", "Categories"),
            ("🛒", "View Orders", "Orders")
        ]

        for i, (icon, text, page) in enumerate(actions):
            action_btn = ctk.CTkButton(
                self.actions_frame,
                text=f"{icon} {text}",
                font=ctk.CTkFont(size=14, weight="bold"),
                height=50,
                corner_radius=10,
                fg_color="#2a2a2a",
                hover_color="#404040",
                command=lambda p=page: self.navigate_to_page(p)
            )
            action_btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")

        # Configure grid weights
        for i in range(len(actions)):
            self.actions_frame.grid_columnconfigure(i, weight=1)

    def refresh_stats(self):
        """Refresh and display statistics"""
        stats = self.controller.get_dashboard_stats()

        # Clear old stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Create enhanced stat cards
        stat_cards = [
            ("📦", "Total Products", str(stats['total_products']), "#007acc"),
            ("📊", "Total Stock", str(stats['total_stock']), "#28a745"),
            ("🛒", "Total Orders", str(stats['total_orders']), "#ffc107"),
            ("💰", "Total Revenue", f"${stats['total_revenue']:.2f}", "#dc3545")
        ]

        for i, (icon, title, value, color) in enumerate(stat_cards):
            self.create_stat_card(i, icon, title, value, color)

        # Refresh graphs
        self.create_product_graph()
        self.create_category_graph()

        # Update datetime
        self.datetime_label.configure(text=datetime.now().strftime("%B %d, %Y • %I:%M %p"))

    def create_stat_card(self, index, icon, title, value, color):
        """Create an enhanced stat card"""
        card = ctk.CTkFrame(
            self.stats_frame,
            fg_color="#2a2a2a",
            border_width=1,
            border_color="#404040",
            corner_radius=15,
            width=200,
            height=120
        )
        card.grid(row=0, column=index, padx=8, pady=8)
        card.grid_propagate(False)

        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=32)
        )
        icon_label.pack(pady=(15, 5))

        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0"
        )
        title_label.pack()

        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(5, 15))

    def create_product_graph(self):
        """Create a graph for product distribution"""
        try:
            # Clear old graphs
            for widget in self.graphs_frame.winfo_children():
                widget.destroy()

            # Get product data from controller
            products = self.controller.get_all_products()

            if not products:
                empty_label = ctk.CTkLabel(
                    self.graphs_frame,
                    text="No product data available",
                    text_color="#a0a0a0",
                    font=ctk.CTkFont(size=14)
                )
                empty_label.pack(fill="both", expand=True, pady=20)
                return

            # Prepare data
            product_names = [p['name'][:15] for p in products]  # Limit name length
            product_stock = [p['stock'] for p in products]

            # Create figure with dark theme
            fig = Figure(figsize=(6, 4), dpi=80, facecolor='#1a1a1a', edgecolor='#2a2a2a')
            ax = fig.add_subplot(111, facecolor='#1a1a1a')

            # Create bar chart
            bars = ax.bar(range(len(product_names)), product_stock, color='#007acc', edgecolor='#404040', linewidth=1.5)

            # Customize chart
            ax.set_xlabel('Products', color='#a0a0a0', fontsize=10)
            ax.set_ylabel('Stock Quantity', color='#a0a0a0', fontsize=10)
            ax.set_title('Product Stock Levels', color='#ffffff', fontsize=12, weight='bold', pad=15)
            ax.set_xticks(range(len(product_names)))
            ax.set_xticklabels(product_names, rotation=45, ha='right', color='#a0a0a0', fontsize=8)
            ax.tick_params(colors='#a0a0a0')
            ax.grid(axis='y', alpha=0.3, color='#404040', linestyle='--')

            # Set spine colors
            for spine in ax.spines.values():
                spine.set_color('#404040')

            fig.tight_layout()

            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=self.graphs_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5, pady=5)

        except Exception as e:
            error_label = ctk.CTkLabel(
                self.graphs_frame,
                text=f"Error loading product graph: {str(e)}",
                text_color="#dc3545",
                font=ctk.CTkFont(size=12)
            )
            error_label.pack(fill="both", expand=True, pady=20)

    def create_category_graph(self):
        """Create a graph for category distribution"""
        try:
            # Get category data from controller
            categories = self.controller.get_all_categories()

            if not categories:
                return

            # Prepare data
            category_names = [c['name'] for c in categories]
            category_counts = [c.get('product_count', 0) for c in categories]

            # Only create if there's data
            if not any(category_counts):
                return

            # Create figure with dark theme
            fig = Figure(figsize=(6, 4), dpi=80, facecolor='#1a1a1a', edgecolor='#2a2a2a')
            ax = fig.add_subplot(111, facecolor='#1a1a1a')

            # Create pie chart
            colors = ['#007acc', '#28a745', '#ffc107', '#dc3545', '#17a2b8', '#6f42c1']
            wedges, texts, autotexts = ax.pie(
                category_counts,
                labels=category_names,
                autopct='%1.1f%%',
                colors=colors[:len(category_names)],
                startangle=90,
                textprops={'color': '#ffffff', 'fontsize': 10}
            )

            # Customize labels
            for autotext in autotexts:
                autotext.set_color('#ffffff')
                autotext.set_weight('bold')
                autotext.set_fontsize(9)

            ax.set_title('Product Distribution by Category', color='#ffffff', fontsize=12, weight='bold', pad=15)

            fig.tight_layout()

            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=self.graphs_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5, pady=5)

        except Exception as e:
            pass  # Silent fail for category graph

    def navigate_to_page(self, page_name):
        """Navigate to the specified page"""
        # This will be handled by the main app's show_page method
        # We need to find the parent window and call its show_page method
        current = self
        while current and not hasattr(current, 'show_page'):
            current = current.master
        if current and hasattr(current, 'show_page'):
            current.show_page(page_name)
