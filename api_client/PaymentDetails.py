import urllib
from urllib import request
from decouple import config
from datetime import datetime
import time
import json

from .Orders import Orders

from .HelperFunctions import getTransactionsByOrder

OUTPUT = []
def getTransactionNode(transaction):
    if 'payment_details' in transaction:
        payment_node = {}
        payment_node['credit_card_number'] = transaction['credit_card_number']
        payment_node['credit_card_company'] = transaction['credit_card_company']
        payment_node['cvv_result_code'] = transactions['cvv_result_code']

        return payment_node
    else:
        return None

def PaymentDetails(order_id):
    """
    Returns a list of dictonary items where each item is a PaymentDetail from an order with required fields
    PaymentDetails( order_id ) where order_id is the unique_id of an order
    """
    global OUTPUT
    data = getTransactionsByOrder(order_id)

    if "error" in data:
        return data 
    
    if "transactions" in data:
        transactions = json_data['transactions']
    else:
        return data 

    for transaction in transactions:
        node = getTransactionNode(transaction)
        if node:
            OUTPUT += node

    return OUTPUT
