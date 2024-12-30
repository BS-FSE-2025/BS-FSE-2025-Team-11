import unittest
from system import OrderSystem

class TestOrderSystem(unittest.TestCase):
    def setUp(self):
        # Preparing initial requests
        self.system = OrderSystem()
        self.system.add_order(1, "אלגברה לינארית", "בהמתנה")
        self.system.add_order(2, "קבוצת כימיה", "מאושר")
        self.system.add_order(3, "English Lesson", "נדחתה")

    def test_get_all_orders(self):
        # Check View All Orders
        orders = self.system.get_all_orders()
        self.assertEqual(len(orders), 3)
        self.assertEqual(orders[0]["subject"], "אלגברה לינארית")

    def test_get_action_for_status(self):
     # Check the appropriate action for each status.
        self.assertEqual(self.system.get_action_for_status("בהמתנה"), "Cancel")
        self.assertEqual(self.system.get_action_for_status("מאושר"), "View Details")
        self.assertEqual(self.system.get_action_for_status("נדחתה"), "Resend")

    def test_get_order_by_id(self):
        order = self.system.get_order_by_id(1)
        self.assertIsNotNone(order)
        self.assertEqual(order["subject"], "אלגברה לינארית")

        #Attempting to access a non-existent request
        order = self.system.get_order_by_id(99)
        self.assertIsNone(order)

if __name__ == "__main__":
    unittest.main()
