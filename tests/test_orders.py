import unittest

from api_client import HelperFunctions
from api_client import Orders
from api_client import LineItems
from api_client import PaymentDetails

class OrdersTests(unittest.TestCase):
    def test_orders_work_without_arguments(self):
        orders = Orders.Orders()
        self.assertEqual(type(orders), type([]))

    def test_get_orders_returns_error_on_invalid_query(self):
        """
        It means orders function should only return orders
        not some other data
        """
        query = "123"
        orders = Orders.getOrders(query, [])
        self.assertIn("errors", orders)

    def test_get_orders_returns_error_on_wrong_query(self):
        """
        It means orders function should only return orders
        not some other data
        """
        query = LineItems.QUERY 
        orders = Orders.getOrders(query, [])
        self.assertIn("errors", orders)

if __name__ == '__main__':
    unittest.main()
