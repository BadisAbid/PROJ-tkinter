from views.base_page import BasePage

class OrderPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, "Order Management")

        # Setup Base Treeview
        self.setup_treeview(("ID", "Product", "Customer", "Quantity", "Total Price", "Date"))

        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        orders = self.controller.order_model.get_all_with_product()
        if orders is None:
            orders = []
        for o in orders:
            self.tree.insert("", "end", values=(o['id'], o['product_name'], o['customer_name'], o['quantity'], f"${o['total_price']:.2f}", o['order_date']))
