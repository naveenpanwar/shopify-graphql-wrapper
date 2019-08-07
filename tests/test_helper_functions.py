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

if __name__ == '__main__':
    unittest.main()
