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
def parseLineItemNode(node):
    output = {}
    output['order_id'] = node['node']['id']
    output['sku'] = node['node']['sku']
    output['price'] = node['node']['originalTotalSet']['shopMoney']['amount']+" "+node['node']['originalTotalSet']['shopMoney']['currencyCode']
    output['title'] = node['node']['title']
    output['quantity'] = node['node']['quantity']
    output['fulfillable_quantity'] = node['node']['fulfillableQuantity']
    output['variant_id'] = node['node']['variant']['id']
    output['properties'] = node['node']['customAttributes']
    output['taxable'] = node['node']['taxable']
    
    tax_lines = []
    for item in node['node']['taxLines']:
        line = {}
        line['price'] = item['priceSet']['shopMoney']['amount']+" "+item['priceSet']['shopMoney']['currencyCode']
        line['rate'] = item['rate']
        line['rate_percentage'] = item['ratePercentage']
        line['title'] = item['title']
        tax_lines.append(line)
    output['tax_lines'] = tax_lines
    
    discounts = []
    for items in node['node']['discountAllocations']:
        discounts.append(item['allocatedAmountSet']['shopMoney']['amount']+" "+item['allocatedAmountSet']['shopMoney']['currencyCode'])
    output['discount_allocations'] = discounts

    return output

def getLineItemsList(data):
    output = []
    raw_data = json.loads(data)
    edges = raw_data['data']['orders']['edges']
    for node in edges:
        lineItems = node['node']['lineItems']['edges']
        for lineItem in lineItems:
            output.append(parseLineItemNode(lineItem))

    return output

def LineItems():
    global query
    data = query.encode('utf-8')
    req = request.Request(api_url, data=data, headers=headers, method="POST")

    response = urllib.request.urlopen(req)
    #getOrdersList(response.read().decode('utf-8'))
    return getLineItemsList(response.read().decode('utf-8'))

print(LineItems())
