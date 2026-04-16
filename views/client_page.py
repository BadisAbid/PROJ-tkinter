import customtkinter as ctk
from tkinter import messagebox
import webbrowser

class ClientPage(ctk.CTkFrame):
    BG     = "#0d0d1a"
    CARD   = "#1a1a2e"
    BORDER = "#3a3a6e"
    ACCENT = "#28a745"  # Green theme for shopping
    TEXT   = "#ccccdd"
    MUTED  = "#888899"

    def __init__(self, parent, controller, user, on_logout):
        super().__init__(parent, fg_color=self.BG)
        self.controller = controller
        self.user = user
        self.on_logout = on_logout
        
        self.cart = {} # Dictionary: {product_id: {"name": str, "price": float, "qty": int}}
        self.all_products = []

        self._build_header()

        # Two columns: left for products, right for cart
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self._build_products_section()
        self._build_cart_section()
        
        self._refresh_products()

    # ==================================================
    #  HEADER
    # ==================================================
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=0, height=60)
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header,
            text="🛒  ShopManager Store",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.ACCENT,
        ).pack(side="left", padx=25, pady=15)

        # Welcome text
        ctk.CTkLabel(
            header,
            text=f"Welcome, {self.user.get('username', 'Client')}!",
            font=ctk.CTkFont(size=14),
            text_color=self.TEXT,
        ).pack(side="left", padx=20)

        # Logout Button
        ctk.CTkButton(
            header, text="🚪  Logout",
            height=34, corner_radius=8,
            fg_color="transparent", hover_color="#3a1a1a", text_color="#e05555",
            command=self.on_logout, width=80
        ).pack(side="right", padx=15)

    # ==================================================
    #  PRODUCTS SECTION (LEFT)
    # ==================================================
    def _build_products_section(self):
        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        left_panel.grid_rowconfigure(1, weight=1) # Scrollable area expands
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Toolbar (Search + Sort/Tri)
        toolbar = ctk.CTkFrame(left_panel, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="🔍  Search products…",
            height=38, corner_radius=10,
            border_color=self.BORDER, fg_color=self.CARD, text_color=self.TEXT, width=240,
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", lambda e: self._filter_and_display())

        ctk.CTkLabel(toolbar, text="Tri (Sort by):", text_color=self.MUTED, font=ctk.CTkFont(size=13)).pack(side="left", padx=(20, 5))
        
        self.sort_var = ctk.StringVar(value="Default")
        sort_combo = ctk.CTkComboBox(
            toolbar,
            values=["Default", "Price: Low to High", "Price: High to Low", "A to Z"],
            variable=self.sort_var,
            command=lambda v: self._filter_and_display(),
            height=38, corner_radius=8,
            border_color=self.BORDER, fg_color=self.CARD, text_color=self.TEXT, button_color=self.ACCENT
        )
        sort_combo.pack(side="left")

        # Scrollable grid for products
        self.products_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent", orientation="horizontal")
        self.products_scroll.grid(row=1, column=0, sticky="nsew")

    # ==================================================
    #  CART SECTION (RIGHT)
    # ==================================================
    def _build_cart_section(self):
        self.cart_panel = ctk.CTkFrame(
            self, fg_color=self.CARD, border_width=1, border_color=self.BORDER, corner_radius=16, width=320
        )
        self.cart_panel.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.cart_panel.grid_propagate(False)
        self.cart_panel.grid_rowconfigure(1, weight=1) # The items area expands

        # Title
        ctk.CTkLabel(
            self.cart_panel, text="🛍️  Your Cart", font=ctk.CTkFont(size=18, weight="bold"), text_color=self.ACCENT
        ).grid(row=0, column=0, pady=(20, 10), padx=20, sticky="w")

        # Items list (scrollable)
        self.cart_items_scroll = ctk.CTkScrollableFrame(self.cart_panel, fg_color="transparent", width=280)
        self.cart_items_scroll.grid(row=1, column=0, sticky="nsew", padx=10)

        # Footer (Total + Checkout)
        footer = ctk.CTkFrame(self.cart_panel, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", pady=15, padx=20)

        self.total_label = ctk.CTkLabel(
            footer, text="Total: 0.00 TND", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.TEXT
        )
        self.total_label.pack(anchor="w", pady=(0, 10))

        ctk.CTkButton(
            footer, text="💳  Checkout Now", height=46, corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.ACCENT, hover_color="#1e7e34",
            command=self._checkout
        ).pack(fill="x")

    # ==================================================
    #  DATA & RENDER
    # ==================================================
    def _refresh_products(self):
        # Fetch all available products
        prods = self.controller.get_products()
        # Filter out out-of-stock items
        self.all_products = [p for p in prods if p.get('stock', 0) > 0] if prods else []
        self._filter_and_display()

    def _filter_and_display(self):
        term = self.search_entry.get().strip().lower()
        
        # 1. Filter by search
        filtered = [p for p in self.all_products if term in p['name'].lower() or term in p.get('category_name', '').lower()]
        
        # 2. Tri (Sort)
        sort_mode = self.sort_var.get()
        if sort_mode == "Price: Low to High":
            filtered.sort(key=lambda x: float(x['price']))
        elif sort_mode == "Price: High to Low":
            filtered.sort(key=lambda x: float(x['price']), reverse=True)
        elif sort_mode == "A to Z":
            filtered.sort(key=lambda x: x['name'].lower())

        # Clear existing
        for w in self.products_scroll.winfo_children():
            w.destroy()

        if not filtered:
            ctk.CTkLabel(
                self.products_scroll, text="No products found matching your criteria.", text_color=self.MUTED, font=ctk.CTkFont(size=14)
            ).grid(row=0, column=0, pady=40, padx=20)
            return

        # 3. Display horizontally
        for idx, prod in enumerate(filtered):
            self._create_product_card(self.products_scroll, prod, 0, idx)

    def _create_product_card(self, parent, prod, row, col):
        card = ctk.CTkFrame(parent, fg_color=self.CARD, border_width=1, border_color=self.BORDER, corner_radius=12, width=200, height=140)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)

        # Truncate long names
        name = prod['name'] if len(prod['name']) <= 18 else prod['name'][:16] + ".."
        ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=14, weight="bold"), text_color=self.TEXT).pack(pady=(15, 2))
        
        cat = prod.get('category_name', 'Misc')
        ctk.CTkLabel(card, text=cat, font=ctk.CTkFont(size=11), text_color=self.MUTED).pack()

        price = float(prod['price'])
        ctk.CTkLabel(card, text=f"{price:.2f} TND", font=ctk.CTkFont(size=16, weight="bold"), text_color=self.ACCENT).pack(pady=(5, 5))

        # Add to cart button
        ctk.CTkButton(
            card, text="Add to Cart", height=30, corner_radius=8, font=ctk.CTkFont(size=12),
            fg_color="#252545", hover_color=self.BORDER, text_color=self.TEXT,
            command=lambda p=prod: self._add_to_cart(p)
        ).pack(fill="x", padx=15, side="bottom", pady=(0, 15))

    # ==================================================
    #  CART LOGIC
    # ==================================================
    def _add_to_cart(self, prod):
        pid = prod['id']
        current_stock = int(prod['stock'])
        
        # Prevent ordering more than stock
        in_cart = self.cart.get(pid, {}).get("qty", 0)
        if in_cart >= current_stock:
            messagebox.showwarning("Out of Stock", f"Only {current_stock} of {prod['name']} available.", parent=self.winfo_toplevel())
            return

        if pid in self.cart:
            self.cart[pid]["qty"] += 1
        else:
            self.cart[pid] = {
                "name": prod['name'],
                "price": float(prod['price']),
                "qty": 1
            }
        self._render_cart()

    def _remove_from_cart(self, pid):
        if pid in self.cart:
            self.cart[pid]["qty"] -= 1
            if self.cart[pid]["qty"] <= 0:
                del self.cart[pid]
            self._render_cart()

    def _render_cart(self):
        # Clear items
        for w in self.cart_items_scroll.winfo_children():
            w.destroy()

        if not self.cart:
            ctk.CTkLabel(self.cart_items_scroll, text="Your cart is empty.", text_color=self.MUTED).pack(pady=30)
            self.total_label.configure(text="Total: 0.00 TND")
            return

        total = 0.0
        for pid, item in self.cart.items():
            subtotal = item["price"] * item["qty"]
            total += subtotal

            row = ctk.CTkFrame(self.cart_items_scroll, fg_color="transparent")
            row.pack(fill="x", pady=8)

            # Name and subtotal
            n = item['name'] if len(item['name']) <= 12 else item['name'][:10]+".."
            ctk.CTkLabel(row, text=f"{n}  (x{item['qty']})", font=ctk.CTkFont(size=13), text_color=self.TEXT).pack(side="left", anchor="w")
            ctk.CTkLabel(row, text=f"{subtotal:.2f} TND", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.TEXT).pack(side="right", padx=(0, 5))

            # Remove button
            ctk.CTkButton(
                row, text="➖", width=25, height=25, corner_radius=6, fg_color="#3a1a1a", hover_color="#7a2020",
                command=lambda p=pid: _remove_safe(p)
            ).pack(side="right", padx=5)
            
        self.total_label.configure(text=f"Total: {total:.2f} TND")

        # Helper so lambda captures current pid properly
        def _remove_safe(p_id):
            self._remove_from_cart(p_id)

    # ==================================================
    #  CHECKOUT
    # ==================================================
    def _checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add some items to your cart first!", parent=self.winfo_toplevel())
            return
            
        confirm = messagebox.askyesno("Checkout", "Place order and proceed to Konnect Payment?", parent=self.winfo_toplevel())
        if not confirm:
            return

        try:
            customer = self.user.get('username', 'Client')
            # Insert each order line into DB, and reduce stock.
            # Order status defaults to 0 (Pending) in the DB automatically
            for pid, item in self.cart.items():
                qty = item['qty']
                total_price = item['price'] * qty
                
                # Create order
                self.controller.order_model.create(pid, customer, qty, total_price)
                
                # Fetch product to decrease stock
                for p in self.all_products:
                    if p['id'] == pid:
                        new_stock = int(p['stock']) - qty
                        self.controller.product_model.update(
                            product_id=pid,
                            category_id=p['category_id'],
                            name=p['name'],
                            price=p['price'],
                            stock=new_stock
                        )
                        break

            # Open Konnect Sandbox Payment Gateway
            webbrowser.open_new("https://sandbox.konnect.network/gateway/")
            
            messagebox.showinfo("Redirecting...", "Your order is placed as Pending (Status 0).\nA browser window has opened for you to complete your secure payment via Konnect Sandbox! 🎉", parent=self.winfo_toplevel())
            
            self.cart.clear()
            self._render_cart()
            self._refresh_products() # Refresh stock
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to checkout:\n{e}", parent=self.winfo_toplevel())
