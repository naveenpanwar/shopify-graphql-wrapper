#some comment
import urllib
from urllib import request
from decouple import config
from datetime import datetime
import time
import json
from HelperFunctions import getQuery

shop_address = config('SHOP_ADDRESS')
access_token = config('ACCESS_TOKEN')

api_url = "https://"+shop_address+".myshopify.com/admin/api/2019-07/graphql.json"
headers = {}
headers["Content-Type"] = "application/graphql"
headers["X-Shopify-Access-Token"] = access_token

OUTPUT = []

QUERY = """
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
    output_node = {}
    output_node['order_id'] = node['node']['id']
    output_node['total_price'] = node['node']['totalPriceSet']['shopMoney']['amount']+" "+node['node']['totalPriceSet']['shopMoney']['currencyCode']
    output_node['name'] = node['node']['name']
    output_node['fulfillment_status'] = node['node']['displayFulfillmentStatus']
    output_node['cursor'] = node['cursor']
    if node['node']['customer']:
        output_node['customer_name'] = node['node']['customer']['displayName']
    else:
        output_node['customer_name'] = None

    return output_node

def getOrdersList(data):
    output_list = []
    edges = data['data']['orders']['edges']

    for node in edges:
        output_list.append(parseOrderNode(node))

    return output_list

def Orders(min_processed_at=None, max_processed_at=None, fulfillment_status=None, cursor=None):
    global OUTPUT
    global QUERY
    query_data = getQuery(QUERY, min_processed_at, max_processed_at, fulfillment_status, cursor)
    req = request.Request(api_url, data=query_data, headers=headers, method="POST")

    response = urllib.request.urlopen(req).read().decode('utf-8')
    
    data = json.loads(response)
    page_info = data['data']['orders']['pageInfo']

    orders_list = getOrdersList(data)
    OUTPUT += orders_list

    if page_info['hasNextPage']:
        Orders(min_processed_at=min_processed_at, max_processed_at=max_processed_at, fulfillment_status=fulfillment_status, cursor=orders_list[-1]['cursor'] )
    
    return OUTPUT
