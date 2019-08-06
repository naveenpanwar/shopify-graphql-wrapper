#some comment
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

output = []

query = """
{
    orders(first: 5 {query} {cursor}) {
        edges {
            cursor
            node {
                id
                processedAt
                totalPriceSet {
                    shopMoney {
                        currencyCode
                        amount
                    }
                }
                name
                displayFulfillmentStatus
                customer {
                    displayName
                }
            }
        }
        pageInfo {
            hasNextPage
        }
    }
}
"""
def parseOrderNode(node):
    output = {}
    output['order_id'] = node['node']['id']
    output['total_price'] = node['node']['totalPriceSet']['shopMoney']['amount']+" "+node['node']['totalPriceSet']['shopMoney']['currencyCode']
    output['name'] = node['node']['name']
    output['fulfillment_status'] = node['node']['displayFulfillmentStatus']
    output['cursor'] = node['cursor']
    if node['node']['customer']:
        output['customer_name'] = node['node']['customer']['displayName']
    else:
        output['customer_name'] = None

    return output

def getOrdersList(data):
    output_list = []
    edges = data['data']['orders']['edges']

    for node in edges:
        output_list.append(parseOrderNode(node))

    return output_list

def getQuery(min_processed_at, max_processed_at, fulfillment_status, cursor):
    global query
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

def Orders(min_processed_at=None, max_processed_at=None, fulfillment_status=None, cursor=None):
    global output
    query = getQuery(min_processed_at, max_processed_at, fulfillment_status, cursor)
    req = request.Request(api_url, data=query, headers=headers, method="POST")

    response = urllib.request.urlopen(req).read().decode('utf-8')
    print(response)
    
    data = json.loads(response)
    page_info = data['data']['orders']['pageInfo']

    if page_info['hasNextPage']:
        orders_list = getOrdersList(data)
        output += orders_list
        Orders(min_processed_at=min_processed_at, max_processed_at=max_processed_at, fulfillment_status=fulfillment_status, cursor=orders_list[-1]['cursor'] )
    print(output)


now = datetime.now()
time.sleep(2)
now2 = datetime.now()
Orders(min_processed_at=now,max_processed_at=now2,fulfillment_status="any")
Orders(min_processed_at=now)
Orders(max_processed_at=now2)
Orders(fulfillment_status="shipped")
Orders()
