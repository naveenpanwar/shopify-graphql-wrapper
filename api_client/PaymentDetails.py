import urllib
from urllib import request
from decouple import config
from datetime import datetime
import time
import json

from Orders import Orders

from HelperFunctions import getTransactionByOrder

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

def PaymentDetails():
    global OUTPUT
    orders_list = Orders()
    for item in orders_list:
        order_id = item['order_id'].split('/')[-1]
        json_data = getTransactionByOrder(order_id)

        transactions = json_data['transactions']

        for transaction in transactions:
            node = getTransactionNode(transaction)
            if node:
                OUTPUT += node

    return OUTPUT
