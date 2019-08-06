#some comment
from HelperFunctions import getQuery, getJSONData

OUTPUT = []

QUERY = """
{
    orders(first: 3 {query} {cursor}) {
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
                    pageInfo {
                        hasNextPage
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
def parseLineItemNode(node, node_cursor):
    line_item_node = {}
    line_item_node['node_cursor'] = node_cursor
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
    edges = data['data']['orders']['edges']
    for node in edges:
        lineItems = node['node']['lineItems']['edges']
        node_cursor = node['cursor']
        for lineItem in lineItems:
            output.append(parseLineItemNode(lineItem, node_cursor))

    return output

def LineItems(min_processed_at=None, max_processed_at=None, fulfillment_status=None, cursor=None):
    global QUERY 
    global OUTPUT

    query_data = getQuery(QUERY, min_processed_at, max_processed_at, fulfillment_status, cursor)
    data = getJSONData(query_data)

    page_info = data['data']['orders']['pageInfo']

    line_items_list = getLineItemsList(data)
    OUTPUT += line_items_list
    
    if page_info['hasNextPage']:
        LineItems(cursor=line_items_list[-1]['node_cursor'] )

    return OUTPUT

print(LineItems())
