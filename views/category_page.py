from views.base_page import BasePage
import customtkinter as ctk

class CategoryPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Category Management")

        # Search Bar
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(fill="x", padx=20, pady=5)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search categories...")
        self.search_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(fill="x", padx=20, pady=5)

        self.add_btn = ctk.CTkButton(self.btn_frame, text="Add Category", command=self.add_category_dialog)
        self.add_btn.pack(side="left", padx=5)

        self.edit_btn = ctk.CTkButton(self.btn_frame, text="Edit Selected", command=self.edit_selected)
        self.edit_btn.pack(side="left", padx=5)

        self.delete_btn = ctk.CTkButton(self.btn_frame, text="Delete Selected", command=self.delete_selected, fg_color="#d32f2f", hover_color="#9a0007")
        self.delete_btn.pack(side="left", padx=5)

        self.export_btn = ctk.CTkButton(self.btn_frame, text="Export CSV", command=self.export_csv)
        self.export_btn.pack(side="left", padx=5)

        # Setup Base Treeview
        self.setup_treeview(("ID", "Name", "Description"))

        self.refresh_table()

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        categories = data if data is not None else self.controller.get_categories()
        if categories is None:
            categories = []
        for cat in categories:
            self.tree.insert("", "end", values=(cat['id'], cat['name'], cat['description']))

    def on_search(self, event):
        term = self.search_entry.get()
        results = self.controller.category_model.search(term)
        self.refresh_table(results)

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a category to edit")
            return
        
        item_id = self.tree.item(selected[0])['values'][0]
        old_name = self.tree.item(selected[0])['values'][1]
        
        dialog = ctk.CTkInputDialog(text=f"Enter New Name for '{old_name}':", title="Edit Category")
        new_name = dialog.get_input()
        if new_name:
            success, msg = self.controller.category_model.update(item_id, new_name, "Updated via Edit")
            if success:
                messagebox.showinfo("Success", "Category updated")
                self.refresh_table()
            else:
                messagebox.showerror("Error", msg)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a category to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this category? (All related products will be deleted)"):
            item_id = self.tree.item(selected[0])['values'][0]
            self.controller.category_model.delete(item_id)
            self.refresh_table()

    def add_category_dialog(self):
        # Implementation for dialog would go here
        dialog = ctk.CTkInputDialog(text="Enter Category Name:", title="Add Category")
        name = dialog.get_input()
        if name:
            success, msg = self.controller.add_category(name, "No description provided")
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_table()
            else:
                messagebox.showerror("Error", msg)

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            categories = self.controller.get_categories()
            if categories:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=categories[0].keys())
                    writer.writeheader()
                    writer.writerows(categories)
                messagebox.showinfo("Export Successful", f"Data exported to {path}")
