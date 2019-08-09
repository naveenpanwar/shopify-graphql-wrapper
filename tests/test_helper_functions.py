import unittest

from api_client import HelperFunctions
from api_client import Orders
from api_client import LineItems
from api_client import PaymentDetails

class HelperFunctionsTests(unittest.TestCase):
    def test_get_query_without_parameters(self):
        s = "orders(first: 5 {query} {cursor})"
        query = HelperFunctions.getQuery(s)
        self.assertEqual(query, b"orders(first: 5  )")
    
    def test_get_query_with_parameters(self):
        s = "orders(first: 5 {query} {cursor})"
        query = HelperFunctions.getQuery(s, fulfillment_status="PENDING")
        self.assertEqual(query, b'''orders(first: 5 , query: "fulfillment_status:PENDING" )''')

    def test_get_query_returns_correct_value_with_only_cursor(self):
        s = "orders(first: 5 {query} {cursor})"
        query = HelperFunctions.getQuery(s, cursor="PENDING")
        self.assertEqual(query, b'''orders(first: 5  , after:\"PENDING\")''')

    def test_get_transations_by_order_returns_dict_with_error_key_on_bad_order_id(self):
        res = HelperFunctions.getTransactionsByOrder("123")
        self.assertEqual(res['error'], "HTTPError, Bad URL or Bad Request")

    def test_get_json_data_returns_dict_with_error_on_bad_url(self):
        res = HelperFunctions.getJSONData("123")
        self.assertEqual(res['error'], "HTTPError, Bad URL or Bad Request")

if __name__ == '__main__':
    unittest.main()
