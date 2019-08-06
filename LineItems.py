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

query = """
{
    orders(first: 3) {
        edges {
            cursor
            node {
                lineItems(first: 20) {
                    edges {
                        cursor
                        node {
                            id
                            sku
                            originalTotalSet {
                                shopMoney {
                                    currencyCode
                                    amount
                                }
                            }
                            title
                            quantity
                            fulfillableQuantity
                            variant {
                                id
                            }
                            customAttributes {
                                key
                                value
                            }
                            taxable
                            taxLines {
                                priceSet {
                                    shopMoney {
                                        currencyCode
                                        amount
                                    }
                                }
                                rate
                                ratePercentage
                                title
                            }
                            discountAllocations {
                                allocatedAmountSet {
                                    shopMoney {
                                        currencyCode
                                        amount
                                    }
                                }
                            }
                        }
                    }
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
    if node['node']['customer']:
        output['customer_name'] = node['node']['customer']['displayName']
    else:
        output['customer_name'] = None

    return output

def getOrdersList(data):
    output = []
    raw_data = json.loads(data)
    edges = raw_data['data']['orders']['edges']
    for node in edges:
        output.append(parseOrderNode(node))

    print(output)

def LineItems():
    global query
    data = query.encode('utf-8')
    req = request.Request(api_url, data=data, headers=headers, method="POST")

    response = urllib.request.urlopen(req)
    #getOrdersList(response.read().decode('utf-8'))
    print(response.read().decode('utf-8'))

LineItems()
