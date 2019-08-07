import urllib
from urllib import request
from decouple import config
import json

def getQuery(query, min_processed_at=None, max_processed_at=None, fulfillment_status=None, cursor=None):
    temp_query_var = query 
    data = query_string = query_wrapper = params = cursor_wrapper = ""
    if min_processed_at or max_processed_at or fulfillment_status:
        query_wrapper+= "query: \"{}\""

    if cursor:
        cursor_wrapper = ", after:"+cursor
        temp_query_var = temp_query_var.replace("{cursor}",cursor_wrapper)
    else:
        temp_query_var = temp_query_var.replace("{cursor}","")

    if min_processed_at:
        params += "processed_at:>"+min_processed_at.strftime("%Y-%m-%dT%H-%M-%SZ")+" "

    if max_processed_at:
        params += "processed_at:<"+max_processed_at.strftime("%Y-%m-%dT%H-%M-%SZ")+" "

    if fulfillment_status:
        params += "fulfillment_status:"+fulfillment_status

    if params != "":
        query_string = query_wrapper.format(params)

    if query_string != "":
        query_string = ", "+query_string
        temp_query_var = temp_query_var.replace("{query}",query_string)
    else:
        temp_query_var = temp_query_var.replace("{query}","")

    return temp_query_var.encode('utf-8')

def getJSONData(query_data):
    shop_address = config('SHOP_ADDRESS')
    access_token = config('ACCESS_TOKEN')

    headers = {}
    headers["Content-Type"] = "application/graphql"
    headers["X-Shopify-Access-Token"] = access_token
    api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/graphql.json"

    req = request.Request(api_url, data=query_data, headers=headers, method="POST")
    
    response = urllib.request.urlopen(req).read().decode('utf-8')
    
    data = json.loads(response)
    return data

def getTransactionByOrder(order_id):
    shop_address = config('SHOP_ADDRESS')
    access_token = config('ACCESS_TOKEN')

    headers = {}
    headers["Content-Type"] = "application/json"
    headers["X-Shopify-Access-Token"] = access_token
    api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/orders/{}/transactions.json"
    data = {}
    url = api_url.format(order_id)
    req = request.Request(url, data=data, headers=headers, method="GET")
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)

    json_data = json.loads(response)
    return json_data
