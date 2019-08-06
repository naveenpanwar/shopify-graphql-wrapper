import urllib
from urllib import request
from decouple import config
from datetime import datetime
import time
import json

shop_address = config('SHOP_ADDRESS')
access_token = config('ACCESS_TOKEN')

api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/orders/1334523592792/transactions.json"
headers = {}
headers["Content-Type"] = "application/json"
headers["X-Shopify-Access-Token"] = access_token

data = {}
    
req = request.Request(api_url, data=data, headers=headers, method="GET")

response = urllib.request.urlopen(req)
#getOrdersList(response.read().decode('utf-8'))
print(response.read().decode('utf-8'))

