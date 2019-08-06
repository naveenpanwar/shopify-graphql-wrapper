from HelperFunctions import getQuery, getJSONData

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
    data = getJSONData(query_data)

    page_info = data['data']['orders']['pageInfo']

    orders_list = getOrdersList(data)
    OUTPUT += orders_list

    if page_info['hasNextPage']:
        Orders(min_processed_at=min_processed_at, max_processed_at=max_processed_at, fulfillment_status=fulfillment_status, cursor=orders_list[-1]['cursor'] )
    
    return OUTPUT

print(Orders())
