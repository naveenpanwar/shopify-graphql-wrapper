#some comment
from .HelperFunctions import getQuery, getJSONData

OUTPUT = []

QUERY = """
{
    order(id: {order_id}) {
        lineItems(first: 2 {cursor}) {
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
            pageInfo {
                hasNextPage
            }
        }
    }
}
"""
def parseLineItemNode(node):
    line_item_node = {}
    line_item_node['cursor'] = node['cursor']
    line_item_node['order_id'] = node['node']['id']
    line_item_node['sku'] = node['node']['sku']
    line_item_node['price'] = node['node']['originalTotalSet']['shopMoney']['amount']+" "+node['node']['originalTotalSet']['shopMoney']['currencyCode']
    line_item_node['title'] = node['node']['title']
    line_item_node['quantity'] = node['node']['quantity']
    line_item_node['fulfillable_quantity'] = node['node']['fulfillableQuantity']
    line_item_node['variant_id'] = node['node']['variant']['id']
    line_item_node['properties'] = node['node']['customAttributes']
    line_item_node['taxable'] = node['node']['taxable']
    
    tax_lines = []
    for item in node['node']['taxLines']:
        line = {}
        line['price'] = item['priceSet']['shopMoney']['amount']+" "+item['priceSet']['shopMoney']['currencyCode']
        line['rate'] = item['rate']
        line['rate_percentage'] = item['ratePercentage']
        line['title'] = item['title']
        tax_lines.append(line)
    line_item_node['tax_lines'] = tax_lines
    
    discounts = []
    for item in node['node']['discountAllocations']:
        discounts.append(item['allocatedAmountSet']['shopMoney']['amount']+" "+item['allocatedAmountSet']['shopMoney']['currencyCode'])
    line_item_node['discount_allocations'] = discounts

    return line_item_node 

def getLineItemsList(data):
    output = []
    edges = data['data']['order']['lineItems']['edges']
    for node in edges:
        output.append(parseLineItemNode(node))

    return output

def LineItems(order_id, cursor=None):
    """
    Returns a list of dictonary items where each item is an LineItem from an order with required fields
    LineItems( order_id ) where order_id is the unique_id of an order
    """
    global QUERY 
    global OUTPUT

    query_data = getQuery(query=QUERY,order_id=order_id, cursor=cursor)
    data = getJSONData(query_data)

    page_info = data['data']['order']['lineItems']['pageInfo']

    line_items_list = getLineItemsList(data)
    OUTPUT += line_items_list
    
    if page_info['hasNextPage']:
        LineItems(order_id=order_id, cursor=line_items_list[-1]['cursor'])

    return OUTPUT
