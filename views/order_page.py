
import customtkinter as ctk
from views.base_page import BasePage
from tkinter import messagebox

# =============================================
#  ORDER PAGE
#  Simple read-only view of all orders.
#  Beginners can see how orders are stored.
# =============================================

class OrderPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "🛒  Order Management")

        # ---- TOOLBAR ----
        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=20, pady=(12, 0))

        ctk.CTkLabel(
            toolbar,
            text="All customer orders are listed below.",
            font=ctk.CTkFont(size=13),
            text_color=self.MUTED,
        ).pack(side="left")

        ctk.CTkButton(
            toolbar, text="🔄  Refresh",
            height=36, corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color=self.CARD, hover_color="#252545",
            border_width=1, border_color=self.BORDER,
            text_color=self.TEXT,
            command=self._refresh,
        ).pack(side="right", padx=(6, 0))

        ctk.CTkButton(
            toolbar, text="📤  Export CSV",
            height=36, corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color="#1a3a2a", hover_color="#1e4a33",
            text_color="#6be585",
            command=self._export,
        ).pack(side="right", padx=(6, 0))

        # ---- TABLE ----
        self.setup_treeview(("ID", "Product", "Quantity", "Total Price", "Status", "Date"))
        self._refresh()

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = []
        try:
            orders = self.controller.order_model.get_all_with_product() or []
        except Exception:
            pass
        for i, o in enumerate(orders):
            tag = "odd" if i % 2 == 0 else "even"
            
            # Format status
            raw_status = o.get("status", 0)
            status_text = "Paid" if raw_status == 1 else "Pending (0)"

            self.tree.insert("", "end",
                             values=(
                                 o.get("id", ""),
                                 o.get("product_name", o.get("product", "")),
                                 o.get("quantity", ""),
                                 o.get("total_price", ""),
                                 status_text,
                                 o.get("order_date", "")
                             ),
                             tags=(tag,))

    def _export(self):
        try:
            orders = self.controller.order_model.get_all_with_product() or []
        except Exception:
            orders = []
        self.export_to_csv(orders, filename_hint="orders")
