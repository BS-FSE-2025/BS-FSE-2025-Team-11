class OrderSystem:
    def __init__(self):
        self.orders = [] #רשימת הבקשות

    def add_order(self, order_id, subject, status):
        self.orders.append({"id": order_id, "subject": subject, "status": status})

    def get_all_orders(self):
        return self.orders

    def get_action_for_status(self, status):
        actions = {
            "בהמתנה": "Cancel",  
            "מאושר": "View Details",  
            "נדחתה": "Resend",  
        }
        return actions.get(status, "No Action")

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order["id"] == order_id:
                return order
        return None
