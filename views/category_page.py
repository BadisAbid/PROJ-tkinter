from views.base_page import BasePage
import customtkinter as ctk
from tkinter import messagebox, filedialog
import csv

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

    def open_category_dialog(self, item_id=None, old_name="", old_desc=""):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Category" if item_id else "Add Category")
        dialog.geometry("380x280")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Name:").pack(pady=(15, 0))
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.pack(pady=(0, 10))
        if old_name:
            name_entry.insert(0, old_name)

        ctk.CTkLabel(dialog, text="Description:").pack(pady=(5, 0))
        desc_entry = ctk.CTkEntry(dialog, width=250)
        desc_entry.pack(pady=(0, 15))
        if old_desc:
            desc_entry.insert(0, old_desc)

        def save():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            if not name:
                messagebox.showwarning("Input Error", "Name is required", parent=dialog)
                return
            try:
                if item_id:
                    self.controller.category_model.update(item_id, name, desc or "No description provided")
                    messagebox.showinfo("Success", "Category updated", parent=dialog)
                else:
                    success, msg = self.controller.add_category(name, desc or "No description provided")
                    if not success:
                        messagebox.showerror("Error", msg, parent=dialog)
                        return
                    messagebox.showinfo("Success", msg, parent=dialog)
                self.refresh_table()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=dialog)

        ctk.CTkButton(dialog, text="Save", command=save).pack(pady=(5, 20))

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a category to edit")
            return
        values = self.tree.item(selected[0])['values']
        self.open_category_dialog(item_id=values[0], old_name=values[1], old_desc=values[2])

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a category to delete")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?\n(All related products will also be deleted)"):
            item_id = self.tree.item(selected[0])['values'][0]
            try:
                self.controller.category_model.delete(item_id)
                self.refresh_table()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def add_category_dialog(self):
        self.open_category_dialog()

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
