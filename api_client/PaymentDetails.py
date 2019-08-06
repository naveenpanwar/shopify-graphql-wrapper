import urllib
from urllib import request
from decouple import config
from datetime import datetime
import time
import json

from Orders import Orders

shop_address = config('SHOP_ADDRESS')
access_token = config('ACCESS_TOKEN')

api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/orders/{}/transactions.json"
headers = {}
headers["Content-Type"] = "application/json"
headers["X-Shopify-Access-Token"] = access_token

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
        data = {}
        order_id = item['order_id'].split('/')[-1]
        url = api_url.format(order_id)
        req = request.Request(url, data=data, headers=headers, method="GET")
        response = urllib.request.urlopen(req).read().decode('utf-8')

        json_data = json.loads(response)
        transactions = json_data['transactions']

        for transaction in transactions:
            node = getTransactionNode(transaction)
            if node:
                OUTPUT += node

    return OUTPUT
