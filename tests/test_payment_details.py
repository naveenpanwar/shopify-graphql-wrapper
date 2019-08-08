import unittest

from api_client import HelperFunctions
from api_client import Orders
from api_client import LineItems
from api_client import PaymentDetails

class PaymentDetailsTests(unittest.TestCase):
    def test_payment_details_returns_dict_with_error_key_on_bad_order_id(self):
        res = HelperFunctions.getTransactionsByOrder("123")
        self.assertEqual(res['error'], "HTTPError, Bad URL or Bad Request")

if __name__ == '__main__':
    unittest.main()
