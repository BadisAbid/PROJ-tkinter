from views.base_page import BasePage
import customtkinter as ctk
from tkinter import messagebox, filedialog
import csv


class ProductPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Product Management")

        # Search Bar
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", padx=20, pady=5)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search products...")
        self.search_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(fill="x", padx=20, pady=5)

        self.add_btn = ctk.CTkButton(self.btn_frame, text="Add Product",
                                     command=self.add_product_dialog)
        self.add_btn.pack(side="left", padx=5)

        self.edit_btn = ctk.CTkButton(self.btn_frame, text="Edit Selected",
                                      command=self.edit_selected)
        self.edit_btn.pack(side="left", padx=5)

        self.delete_btn = ctk.CTkButton(self.btn_frame, text="Delete Selected",
                                        command=self.delete_product,
                                        fg_color="#d32f2f", hover_color="#9a0007")
        self.delete_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(self.btn_frame, text="Export CSV",
                                        command=self.export_csv)
        self.export_btn.pack(side="left", padx=5)

        # Treeview
        self.setup_treeview(("ID", "Name", "Category", "Price", "Stock"))
        self.refresh_table()

    # ── helpers ────────────────────────────────────────────────────────────────

    def get_category_id_by_name(self, name):
        cats = self.controller.get_categories()
        if not cats:
            return None
        for c in cats:
            if c['name'] == name:
                return c['id']
        return None

    def product_name_exists(self, name, exclude_id=None):
        """Return True if a product with this name already exists."""
        products = self.controller.get_products()
        if not products:
            return False
        for p in products:
            if p['name'].strip().lower() == name.strip().lower():
                if exclude_id is not None and p['id'] == exclude_id:
                    continue
                return True
        return False

    # ── table ──────────────────────────────────────────────────────────────────

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        products = self.controller.get_products()
        if not products:
            products = []
        for p in products:
            self.tree.insert("", "end",
                             values=(p['id'], p['name'], p['category_name'],
                                     p['price'], p['stock']))

    def on_search(self, event):
        term = self.search_entry.get()
        results = self.controller.product_model.search(term)
        for item in self.tree.get_children():
            self.tree.delete(item)
        if results:
            for p in results:
                self.tree.insert("", "end",
                                 values=(p['id'], p['name'], p['category_name'],
                                         p['price'], p['stock']))

    # ── dialogs ────────────────────────────────────────────────────────────────

    def open_product_dialog(self, item_id=None, item_values=None):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Product" if item_id else "Add Product")
        dialog.geometry("400x420")
        dialog.transient(self)
        dialog.grab_set()

        # Name
        ctk.CTkLabel(dialog, text="Name:").pack(pady=(15, 0))
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.pack(pady=(0, 10))
        if item_values:
            name_entry.insert(0, item_values[1])

        # Category
        ctk.CTkLabel(dialog, text="Category:").pack(pady=(5, 0))
        cats = self.controller.get_categories()
        cat_names = [c['name'] for c in cats] if cats else []
        cat_combo = ctk.CTkComboBox(dialog, values=cat_names, width=250)
        cat_combo.pack(pady=(0, 10))
        if item_values:
            cat_combo.set(item_values[2])
        elif cat_names:
            cat_combo.set(cat_names[0])

        # Price
        ctk.CTkLabel(dialog, text="Price:").pack(pady=(5, 0))
        price_entry = ctk.CTkEntry(dialog, width=250)
        price_entry.pack(pady=(0, 10))
        if item_values:
            price_entry.insert(0, item_values[3])

        # Stock
        ctk.CTkLabel(dialog, text="Stock:").pack(pady=(5, 0))
        stock_entry = ctk.CTkEntry(dialog, width=250)
        stock_entry.pack(pady=(0, 15))
        if item_values:
            stock_entry.insert(0, item_values[4])

        def save():
            name  = name_entry.get().strip()
            price = price_entry.get().strip()
            stock = stock_entry.get().strip()
            cat_name = cat_combo.get()
            cat_id   = self.get_category_id_by_name(cat_name)

            if not name or not price or not stock:
                messagebox.showwarning("Input Error", "Please fill in all fields.",
                                       parent=dialog)
                return

            if not cat_id:
                messagebox.showerror("Error", "Please select a valid category.",
                                     parent=dialog)
                return

            # Duplicate check (skip current item when editing)
            if self.product_name_exists(name, exclude_id=item_id):
                messagebox.showwarning("Duplicate",
                                       f"A product named '{name}' already exists.",
                                       parent=dialog)
                return

            try:
                if item_id:
                    self.controller.product_model.update(
                        item_id, cat_id, name, price, stock)
                    messagebox.showinfo("Success", "Product updated.", parent=dialog)
                else:
                    success, msg = self.controller.add_product(
                        cat_id, name, price, stock)
                    if not success:
                        messagebox.showerror("Error", msg, parent=dialog)
                        return
                    messagebox.showinfo("Success", msg, parent=dialog)
                self.refresh_table()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ctk.CTkButton(dialog, text="Save", command=save, width=150).pack(pady=(5, 20))

    # ── actions ────────────────────────────────────────────────────────────────

    def add_product_dialog(self):
        self.open_product_dialog()

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit.")
            return
        item_values = self.tree.item(selected[0])['values']
        self.open_product_dialog(item_id=item_values[0], item_values=item_values)

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete.")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this product?"):
            item_id = self.tree.item(selected[0])['values'][0]
            try:
                self.controller.product_model.delete(item_id)
                self.refresh_table()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
        if path:
            products = self.controller.get_products()
            if products:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=products[0].keys())
                    writer.writeheader()
                    writer.writerows(products)
                messagebox.showinfo("Export Successful", f"Data exported to:\n{path}")
