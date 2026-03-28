from models.category_model import CategoryModel
from models.product_model import ProductModel
from models.order_model import OrderModel

class MainController:
    def __init__(self):
        self.category_model = CategoryModel()
        self.product_model = ProductModel()
        self.order_model = OrderModel()

    # Category Actions
    def get_categories(self):
        return self.category_model.get_all()

    def add_category(self, name, description):
        if not name:
            return False, "Name is required"
        try:
            self.category_model.create(name, description)
            return True, "Category added successfully"
        except Exception as e:
            return False, str(e)

    # Product Actions
    def get_products(self):
        return self.product_model.get_all_with_category()

    def add_product(self, category_id, name, price, stock):
        if not name or not category_id:
            return False, "Name and Category are required"
        try:
            self.product_model.create(category_id, name, price, stock)
            return True, "Product added successfully"
        except Exception as e:
            return False, str(e)

    # Dashboard Stats
    def get_dashboard_stats(self):
        prod_stats = self.product_model.get_stats()
        order_stats = self.order_model.get_stats()
        
        return {
            'total_products': prod_stats.get('total_count', 0) if prod_stats else 0,
            'total_stock': prod_stats.get('total_stock', 0) if prod_stats else 0,
            'total_orders': order_stats.get('order_count', 0) if order_stats else 0,
            'total_revenue': float(order_stats.get('total_revenue', 0) or 0) if order_stats else 0.0
        }
