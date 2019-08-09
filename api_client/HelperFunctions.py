import urllib
from urllib import request
from decouple import config
import json

shop_address = config('SHOP_ADDRESS')
access_token = config('ACCESS_TOKEN')
    
headers = {}
headers["X-Shopify-Access-Token"] = access_token

def getQuery(query, min_processed_at=None, max_processed_at=None, fulfillment_status=None, cursor=None, order_id=None):
    temp_query_var = query 
    data = query_string = query_wrapper = params = cursor_wrapper = ""
    if min_processed_at or max_processed_at or fulfillment_status:
        query_wrapper+= "query: \"{}\""

    if order_id:
        order_id = "\""+order_id+"\""
        temp_query_var = temp_query_var.replace("{order_id}",order_id)

    if cursor:
        cursor_wrapper = ", after:\""+cursor+"\""
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

def getResponse( request ):
    try:
        response = urllib.request.urlopen(request).read().decode('utf-8')
    except urllib.error.HTTPError:
        response = "{\"error\": \"HTTPError, Bad URL or Bad Request\"}"

    return response

def getDecodedJson( response ):
    try:
        data = json.loads(response)
    except json.decoder.JSONDecodeError:
        data = json.loads("{\"error\": \"Cannot decode JSON data\"}")

    return json_data

def getJSONData( query_data ):
    global shop_address, access_token, headers

    local_headers = headers
    local_headers["Content-Type"] = "application/graphql"
    api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/graphql.json"

    req = request.Request(api_url, data=query_data, headers=local_headers, method="POST")
    
    response = getResponse( req )
    data = getDecodedJson( response )
    return data

def getTransactionsByOrder( order_id ):
    global shop_address, access_token, headers
    
    local_headers = headers
    local_headers["Content-Type"] = "application/json"
    api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/orders/{}/transactions.json"
    url = api_url.format(order_id)
    req = request.Request(url, data={}, headers=local_headers, method="GET")
    
    response = getResponse( req )
    data = getDecodedJson( response )
    return data
