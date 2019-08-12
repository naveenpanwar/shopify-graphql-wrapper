import unittest

from api_client import HelperFunctions
from api_client import Orders
from api_client import LineItems
from api_client import PaymentDetails

class LineItemsTests(unittest.TestCase):
    def test_line_items_have_to_have_correct_order_id(self):
        line_items = LineItems.LineItems('some_order_id')
        self.assertIn('errors', line_items)

    def test_get_line_items_returns_error_on_invalid_query(self):
        query = "123"
        line_items = LineItems.getLineItems(query, [], 'some_order_id')
        self.assertIn("errors", line_items)

    def test_get_orders_returns_error_on_wrong_query(self):
        query = Orders.QUERY 
        line_items = LineItems.getLineItems(query, [], 'some_order_id')
        self.assertIn("errors", line_items)

if __name__ == '__main__':
    unittest.main()
