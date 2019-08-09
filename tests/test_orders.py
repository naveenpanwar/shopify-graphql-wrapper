import unittest

from api_client import HelperFunctions
from api_client import Orders
from api_client import LineItems
from api_client import PaymentDetails

class OrdersTests(unittest.TestCase):
    def test_orders_work_without_arguments(self):
        orders = Orders.Orders()
        self.assertEqual(type(orders), type([]))

if __name__ == '__main__':
    unittest.main()
