import urllib
from urllib import request
from decouple import config
from datetime import datetime
import time
import json

shop_address = config('SHOP_ADDRESS')
access_token = config('ACCESS_TOKEN')

api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/graphql.json"
headers = {}
headers["Content-Type"] = "application/graphql"
headers["X-Shopify-Access-Token"] = access_token

