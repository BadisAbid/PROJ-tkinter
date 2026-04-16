
import customtkinter as ctk
from tkinter import messagebox
from views.base_page import BasePage

# =============================================
#  PRODUCT PAGE
#  Users can add, edit, delete and search
#  products. A side panel slides in to let
#  the user fill in product details.
# =============================================

class ProductPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "📦  Product Management")

        # We'll use a two-column layout:
        #   left  = search + table
        #   right = "Add / Edit" panel
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.body.grid_columnconfigure(0, weight=1)   # table side grows
        self.body.grid_columnconfigure(1, weight=0)   # panel side is fixed
        self.body.grid_rowconfigure(0, weight=1)

        # Build the left table area and the right input panel
        self._build_table_side()
        self._build_input_panel()

        # Load all products into the table
        self._refresh_table()

    # ==================================================
    #  LEFT SIDE — search bar + action buttons + table
    # ==================================================

    def _build_table_side(self):
        left = ctk.CTkFrame(self.body, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        # ---- TOOLBAR ----
        toolbar = ctk.CTkFrame(left, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        # Search box
        self.search_entry = ctk.CTkEntry(
            toolbar,
            placeholder_text="🔍  Search products…",
            height=38, corner_radius=10,
            border_color=self.BORDER, fg_color=self.CARD,
            text_color=self.TEXT, font=ctk.CTkFont(size=13),
            width=220,
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self._on_search)

        btn_cfg = dict(height=38, corner_radius=10, font=ctk.CTkFont(size=13, weight="bold"))

        # "Edit" button (loads selected row into the panel)
        ctk.CTkButton(
            toolbar, text="✏️  Edit",
            fg_color="#252545", hover_color=self.BORDER, text_color=self.TEXT,
            command=self._load_selected_for_edit, **btn_cfg,
        ).pack(side="right", padx=(6, 0))

        # "Delete" button
        ctk.CTkButton(
            toolbar, text="🗑️  Delete",
            fg_color="#4a1a1a", hover_color="#7a2020", text_color="#ff6b6b",
            command=self._delete_selected, **btn_cfg,
        ).pack(side="right", padx=(6, 0))

        # "Export CSV" button
        ctk.CTkButton(
            toolbar, text="📤  Export CSV",
            fg_color="#1a3a2a", hover_color="#1e4a33", text_color="#6be585",
            command=self._export, **btn_cfg,
        ).pack(side="right", padx=(6, 0))

        # "New Product" button — opens the panel pre-cleared
        ctk.CTkButton(
            toolbar, text="➕  New Product",
            fg_color=self.ACCENT, hover_color="#5a60d0",
            command=self._reset_panel, **btn_cfg,
        ).pack(side="right", padx=(6, 0))

        # ---- TABLE ----
        # We re-use the base-class helper but point it at `left`
        # so we draw it inside our grid instead of self
        self.tree_frame = ctk.CTkFrame(left, fg_color=self.CARD, corner_radius=12)
        self.tree_frame.grid(row=1, column=0, sticky="nsew")

        from tkinter import ttk
        style = __import__("tkinter.ttk", fromlist=["Style"]).Style()
        style.theme_use("clam")
        style.configure("Prod.Treeview",
            background="#1a1a2e", foreground="#ccccdd",
            fieldbackground="#1a1a2e", rowheight=34,
            font=("Segoe UI", 12), borderwidth=0)
        style.configure("Prod.Treeview.Heading",
            background="#252545", foreground="#7c83fd",
            font=("Segoe UI", 12, "bold"), relief="flat")
        style.map("Prod.Treeview",
            background=[("selected", "#3a3a6e")],
            foreground=[("selected", "#ffffff")])

        cols = ("ID", "Name", "Category", "Price", "Stock")
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, show="headings", style="Prod.Treeview")
        widths = {"ID": 50, "Name": 200, "Category": 160, "Price": 90, "Stock": 80}
        for col in cols:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_column(c, False))
            self.tree.column(col, width=widths.get(col, 120), anchor="center")
        self.tree.tag_configure("odd",  background="#1e1e38")
        self.tree.tag_configure("even", background="#1a1a2e")

        sb = __import__("tkinter.ttk", fromlist=["Scrollbar"]).Scrollbar(
            self.tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y", padx=(0, 4), pady=8)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # Double-click on a row to load it into the edit panel
        self.tree.bind("<Double-1>", lambda e: self._load_selected_for_edit())

    # ==================================================
    #  RIGHT SIDE — Add / Edit panel
    # ==================================================

    def _build_input_panel(self):
        """Create the side panel where users fill in product details."""
        self.panel = ctk.CTkFrame(
            self.body,
            fg_color=self.CARD,
            border_width=1,
            border_color=self.BORDER,
            corner_radius=16,
            width=280,
        )
        self.panel.grid(row=0, column=1, sticky="nsew")
        self.panel.grid_propagate(False)

        # Panel title
        self.panel_title = ctk.CTkLabel(
            self.panel,
            text="➕  New Product",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.ACCENT,
        )
        self.panel_title.pack(pady=(22, 14), padx=20, anchor="w")

        # ---- NAME ----
        ctk.CTkLabel(self.panel, text="Product Name", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=self.TEXT, anchor="w").pack(fill="x", padx=20)
        self.name_entry = ctk.CTkEntry(
            self.panel, placeholder_text="e.g. Apple Juice",
            height=38, corner_radius=8,
            border_color=self.BORDER, fg_color="#252545", text_color="#fff",
        )
        self.name_entry.pack(fill="x", padx=20, pady=(4, 12))

        # ---- CATEGORY ----
        ctk.CTkLabel(self.panel, text="Category", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=self.TEXT, anchor="w").pack(fill="x", padx=20)
        cats = self.controller.get_categories() or []
        self._cat_names = [c["name"] for c in cats]
        self.cat_combo = ctk.CTkComboBox(
            self.panel,
            values=self._cat_names or ["No categories yet"],
            height=38, corner_radius=8,
            border_color=self.BORDER, fg_color="#252545",
            text_color="#fff", button_color=self.ACCENT,
            dropdown_fg_color="#1a1a2e",
        )
        if self._cat_names:
            self.cat_combo.set(self._cat_names[0])
        self.cat_combo.pack(fill="x", padx=20, pady=(4, 12))

        # ---- PRICE ----
        ctk.CTkLabel(self.panel, text="Price (TND)", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=self.TEXT, anchor="w").pack(fill="x", padx=20)
        self.price_entry = ctk.CTkEntry(
            self.panel, placeholder_text="e.g. 12.99",
            height=38, corner_radius=8,
            border_color=self.BORDER, fg_color="#252545", text_color="#fff",
        )
        self.price_entry.pack(fill="x", padx=20, pady=(4, 12))

        # ---- STOCK ----
        ctk.CTkLabel(self.panel, text="Stock Quantity", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=self.TEXT, anchor="w").pack(fill="x", padx=20)
        self.stock_entry = ctk.CTkEntry(
            self.panel, placeholder_text="e.g. 50",
            height=38, corner_radius=8,
            border_color=self.BORDER, fg_color="#252545", text_color="#fff",
        )
        self.stock_entry.pack(fill="x", padx=20, pady=(4, 20))

        # ---- SAVE BUTTON ----
        self.save_btn = ctk.CTkButton(
            self.panel, text="💾  Save Product",
            height=42, corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.ACCENT, hover_color="#5a60d0",
            command=self._save_product,
        )
        self.save_btn.pack(fill="x", padx=20)

        # ---- CLEAR BUTTON ----
        ctk.CTkButton(
            self.panel, text="✖  Clear Form",
            height=36, corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color="transparent", hover_color="#252545",
            text_color=self.MUTED, border_width=1, border_color=self.BORDER,
            command=self._reset_panel,
        ).pack(fill="x", padx=20, pady=(8, 0))

        # Hidden: track which product is being edited (None = add mode)
        self._editing_id = None

    # ==================================================
    #  TABLE HELPERS
    # ==================================================

    def _refresh_table(self, data=None):
        """Clear and reload the product table."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        products = data if data is not None else (self.controller.get_products() or [])
        for i, p in enumerate(products):
            tag = "odd" if i % 2 == 0 else "even"
            self.tree.insert("", "end",
                             values=(p["id"], p["name"], p.get("category_name", ""),
                                     p["price"], p["stock"]),
                             tags=(tag,))

    def _on_search(self, _event=None):
        term = self.search_entry.get().strip()
        results = self.controller.product_model.search(term)
        self._refresh_table(results)

    def insert_row(self, values):
        """Override BasePage insert_row so it works with self.tree here too."""
        count = len(self.tree.get_children())
        tag = "odd" if count % 2 == 0 else "even"
        self.tree.insert("", "end", values=values, tags=(tag,))

    # ==================================================
    #  PANEL HELPERS
    # ==================================================

    def _reset_panel(self):
        """Clear all form fields and switch to 'Add' mode."""
        self._editing_id = None
        self.panel_title.configure(text="➕  New Product")
        self.save_btn.configure(text="💾  Save Product", fg_color=self.ACCENT)
        self.name_entry.delete(0, "end")
        self.price_entry.delete(0, "end")
        self.stock_entry.delete(0, "end")
        # Refresh category list in case new ones were added
        cats = self.controller.get_categories() or []
        self._cat_names = [c["name"] for c in cats]
        self.cat_combo.configure(values=self._cat_names or ["No categories yet"])
        if self._cat_names:
            self.cat_combo.set(self._cat_names[0])

    def _load_selected_for_edit(self):
        """Fill the panel with the selected product's data."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Nothing selected",
                                   "Please click on a product row first.", parent=self.winfo_toplevel())
            return
        vals = self.tree.item(selected[0])["values"]
        # vals = (id, name, category_name, price, stock)
        self._editing_id = vals[0]
        self.panel_title.configure(text=f"✏️  Edit: {vals[1]}")
        self.save_btn.configure(text="💾  Update Product", fg_color="#e67e22")

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, str(vals[1]))

        # Set category dropdown
        cats = self.controller.get_categories() or []
        self._cat_names = [c["name"] for c in cats]
        self.cat_combo.configure(values=self._cat_names)
        self.cat_combo.set(str(vals[2]))

        self.price_entry.delete(0, "end")
        self.price_entry.insert(0, str(vals[3]))

        self.stock_entry.delete(0, "end")
        self.stock_entry.insert(0, str(vals[4]))

    def _get_cat_id(self, name):
        """Return the category ID for a given category name."""
        for c in (self.controller.get_categories() or []):
            if c["name"] == name:
                return c["id"]
        return None

    # ==================================================
    #  ACTIONS
    # ==================================================

    def _save_product(self):
        """Validate inputs and save (add or update) the product."""
        name  = self.name_entry.get().strip()
        price = self.price_entry.get().strip()
        stock = self.stock_entry.get().strip()
        cat_name = self.cat_combo.get()
        cat_id   = self._get_cat_id(cat_name)

        # --- Validate ---
        if not name:
            messagebox.showwarning("Missing Field", "Please enter a product name.", parent=self.winfo_toplevel())
            return
        if not cat_id:
            messagebox.showwarning("No Category", "Please select a valid category.\nGo to 'Categories' to add one first.", parent=self.winfo_toplevel())
            return
        try:
            price_val = float(price)
            if price_val < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Price", "Price must be a positive number (e.g. 9.99).", parent=self.winfo_toplevel())
            return
        try:
            stock_val = int(stock)
            if stock_val < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Stock", "Stock must be a whole positive number (e.g. 50).", parent=self.winfo_toplevel())
            return

        try:
            if self._editing_id:
                # UPDATE existing product
                self.controller.product_model.update(
                    self._editing_id, cat_id, name, price_val, stock_val)
                messagebox.showinfo("Updated ✅", f"'{name}' has been updated!", parent=self.winfo_toplevel())
            else:
                # ADD new product
                ok, msg = self.controller.add_product(cat_id, name, price_val, stock_val)
                if not ok:
                    messagebox.showerror("Error", msg, parent=self.winfo_toplevel())
                    return
                messagebox.showinfo("Added ✅", f"'{name}' has been added!", parent=self.winfo_toplevel())

            self._refresh_table()
            self._reset_panel()

        except Exception as err:
            messagebox.showerror("Error", str(err), parent=self.winfo_toplevel())

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Nothing selected",
                                   "Please click on a product row first.", parent=self.winfo_toplevel())
            return
        vals = self.tree.item(selected[0])["values"]
        if messagebox.askyesno("Delete Product",
                               f"Are you sure you want to delete  '{vals[1]}'?",
                               parent=self.winfo_toplevel()):
            try:
                self.controller.product_model.delete(vals[0])
                self._refresh_table()
                self._reset_panel()
            except Exception as err:
                messagebox.showerror("Error", str(err), parent=self.winfo_toplevel())

    def _export(self):
        self.export_to_csv(self.controller.get_products() or [], filename_hint="products")
