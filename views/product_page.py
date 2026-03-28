from views.base_page import BasePage

class ProductPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Product Management")

        # Form Frame
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.form_frame, text="Price:").grid(row=0, column=2, padx=5, pady=5)
        self.price_entry = ctk.CTkEntry(self.form_frame)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(self.form_frame, text="Stock:").grid(row=0, column=4, padx=5, pady=5)
        self.stock_entry = ctk.CTkEntry(self.form_frame)
        self.stock_entry.grid(row=0, column=5, padx=5, pady=5)

        self.save_btn = ctk.CTkButton(self.form_frame, text="Add Product", command=self.add_product)
        self.save_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=5)

        self.update_btn = ctk.CTkButton(self.form_frame, text="Update Selected", command=self.update_product)
        self.update_btn.grid(row=1, column=2, columnspan=2, pady=10, padx=5)

        self.del_btn = ctk.CTkButton(self.form_frame, text="Delete Selected", command=self.delete_product, fg_color="#d32f2f", hover_color="#9a0007")
        self.del_btn.grid(row=1, column=4, columnspan=2, pady=10, padx=5)

        # Setup Base Treeview
        self.setup_treeview(("ID", "Name", "Category", "Price", "Stock"))

        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        products = self.controller.get_products()
        if products is None:
            products = []
        for p in products:
            self.tree.insert("", "end", values=(p['id'], p['name'], p['category_name'], p['price'], p['stock']))

    def update_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to update")
            return
        
        item_id = self.tree.item(selected[0])['values'][0]
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()
        
        if name and price and stock:
            cats = self.controller.get_categories()
            success = self.controller.product_model.update(item_id, cats[0]['id'], name, price, stock)
            if success:
                messagebox.showinfo("Success", "Product updated")
                self.refresh_table()
        else:
            messagebox.showwarning("Input Error", "Fill in all fields to update")

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete this product?"):
            item_id = self.tree.item(selected[0])['values'][0]
            self.controller.product_model.delete(item_id)
            self.refresh_table()

    def add_product(self):
        # Simplistic category selection for now (picking first category or hardcoded for demo)
        cats = self.controller.get_categories()
        if not cats:
            messagebox.showerror("Error", "Please add a category first")
            return
        
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()
        
        if name and price and stock:
            success, msg = self.controller.add_product(cats[0]['id'], name, price, stock)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_table()
            else:
                messagebox.showerror("Error", msg)
